
using System;
using System.Collections;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;
using System.Net.Sockets;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;
using ChatApp.Model;
using ChatApp.View;
using ChatApp.View.Command;

namespace ChatApp.ViewModel
{
    internal class MainWindowViewModel : INotifyPropertyChanged
    {
        private NetworkManager NetworkManager { get; set; }

        private ChatHistoryManager chatHistoryManager = new ChatHistoryManager();
        public ObservableCollection<ChatHistory> ChatHistoryItems { get; set; } = new ObservableCollection<ChatHistory>();
        private ChatHistory selectedChatHistory;
        public ChatHistory SelectedChatHistory
        {
            get { return selectedChatHistory; }
            set
            {
                selectedChatHistory = value;
                OnPropertyChanged();
                LoadChatHistory(selectedChatHistory);
            }
        }
        private string searchQuery;
        public string SearchQuery
        {
            get { return searchQuery; }
            set
            {
                searchQuery = value;
                OnPropertyChanged();
                SearchChatHistory(searchQuery);
            }
        }

        private ICommand startServer;
        private ICommand startClient;
        private ICommand enterCommand;
        private ICommand inviteAccept;
        private ICommand inviteDecline;
        private ICommand buzzCommand;

        private ChatWindow chatWindow;

        private string text;
        private string toptext = "Welcome the ChatApp!";
        private string userName = "";
        private int? portNum = null;
        private string ipAdd = "127.0.0.1";
        private string statusText;

        public string MyText
        {
            get => text;
            set
            {
                text = value;
                OnPropertyChanged(nameof(MyText));
            }
        }

        public string TopText
        {
            get => toptext;
            set
            {
                toptext = value;
                OnPropertyChanged(nameof(TopText));
            }
        }

        public string UserName
        {
            get => userName;
            set
            {
                userName = value;
                OnPropertyChanged(nameof(UserName));
            }
        }

        public int? PortNum
        {
            get => portNum;
            set
            {
                portNum = value;
                OnPropertyChanged(nameof(PortNum));
            }
        }

        public string IpAdd
        {
            get => ipAdd;
            set
            {
                ipAdd = value;
                OnPropertyChanged(nameof(IpAdd));
            }
        }

        public string StatusText
        {
            get => statusText;
            set
            {
                statusText = value;
                OnPropertyChanged(nameof(StatusText));
            }
        }



        public ObservableCollection<string> Messages { get; set; } = new ObservableCollection<string>();



        private Visibility acceptButtonVisibility = Visibility.Hidden;
        public Visibility AcceptButtonVisibility
        {
            get { return acceptButtonVisibility; }
            set
            {
                if (acceptButtonVisibility != value)
                {
                    acceptButtonVisibility = value;
                    OnPropertyChanged();
                }
            }
        }

        private Visibility declineButtonVisibility = Visibility.Hidden;
        public Visibility DeclineButtonVisibility
        {
            get { return declineButtonVisibility; }
            set
            {
                if (declineButtonVisibility != value)
                {
                    declineButtonVisibility = value;
                    OnPropertyChanged();
                }
            }
        }

        private bool acceptButtonEnabled = false;
        public bool AcceptButtonEnabled
        {
            get { return acceptButtonEnabled; }
            set
            {
                if (acceptButtonEnabled != value)
                {
                    acceptButtonEnabled = value;
                    OnPropertyChanged();
                }
            }
        }

        private bool declineButtonEnabled = false;
        public bool DeclineButtonEnabled
        {
            get { return declineButtonEnabled; }
            set
            {
                if (declineButtonEnabled != value)
                {
                    declineButtonEnabled = value;
                    OnPropertyChanged();
                }
            }
        }


        public event PropertyChangedEventHandler PropertyChanged;
        private void OnPropertyChanged([CallerMemberName] string propertyName = "")
        {
            if (PropertyChanged != null)
            {
                PropertyChanged(this, new PropertyChangedEventArgs(propertyName));
            }
        }

        private void ChatWindow_Closing(object sender, CancelEventArgs e)
        {
            NetworkManager.SendDisconnectMessage(UserName);
            Application.Current.Dispatcher.Invoke(() =>
            {
                Application.Current.MainWindow.Visibility = Visibility.Visible;
                TopText = "ChatWindow closed.";
            });
            NetworkManager.Stop();
        }

        public MainWindowViewModel(NetworkManager networkManager)
        {
            NetworkManager = networkManager;
            NetworkManager.Initialize(this);
            networkManager.PropertyChanged += myModel_PropertyChanged;
        }

        private void myModel_PropertyChanged(object sender, PropertyChangedEventArgs e)
        {
            Application.Current?.Dispatcher.Invoke(() =>
            {
                switch (e.PropertyName)
                {
                    case "Message":
                        var message = NetworkManager.Message;
                        Messages.Add($"{message}");
                        break;

                    case "acceptInvite":
                        showChatWindow();
                        break;

                    case "declineInvite":
                        updateTopText("Declined");
                        break;

                    case "activeRequest":
                        if (NetworkManager.ActiveRequest)
                        {
                            showButtons(true);
                        }
                        break;

                    case "status":
                        var status = NetworkManager.Status;
                        UpdateStatusText(status);
                        break;

                    case "Toptext":
                        TopText = NetworkManager.Toptext;
                        break;
                }
            });
        }


        public ICommand StartClient
        {
            get
            {
                if (startClient == null)
                    startClient = new StartClientCommand(this);
                return startClient;
            }
            set
            {
                startClient = value;
            }
        }

        public ICommand StartServer
        {
            get
            {
                if (startServer == null)
                    startServer = new StartServerCommand(this);
                return startServer;
            }
            set
            {
                startServer = value;
            }
        }

        public ICommand EnterCommand
        {
            get
            {
                if (enterCommand == null)
                {
                    return new Command.KeyEnterCommand(this);
                }
                else
                {
                    return enterCommand;
                }
            }
            set
            {
                enterCommand = value;
            }
        }
        public ICommand BuzzCommand
        {
            get
            {
                if (buzzCommand == null)
                {
                    return new Command.BuzzCommand(this);
                }
                else
                { return buzzCommand; }
            }
            set
            { buzzCommand = value; }
        }

        public ICommand InviteAccept
        {
            get
            {
                if (inviteAccept == null)
                {
                    return new Command.AcceptCommand(this);
                }
                else { return inviteAccept; }
            }
            set { inviteAccept = value; }
        }

        public ICommand InviteDecline
        {
            get
            {
                if (inviteDecline == null)
                {
                    return new Command.DeclineCommand(this);
                }
                else { return inviteDecline; }
            }
            set { inviteDecline = value; }
        }



        public void startHost()
        {
            if (!PortNum.HasValue)
            {
                TopText = "Please enter a port number!";
                return;
            }

            int port = PortNum.Value;

            if (NetworkManager.startHost(UserName, port, IpAdd))
            {
                Application.Current.Dispatcher.Invoke(() =>
                {
                    showChatWindow();
                    TopText = $"Hosting server on port {PortNum}.";
                });
            }
            else
            {
                Application.Current.Dispatcher.Invoke(() =>
                {
                    TopText = NetworkManager.Toptext;
                });
            }

        }

        public void startConnection()
        {

            if (!PortNum.HasValue)
            {
                TopText = "Please enter a port number!";
                return;
            }

            int port = PortNum.Value;

            
            Task.Run(() =>
            {
                var status = NetworkManager.startConnection(UserName, port, IpAdd);

                Application.Current.Dispatcher.Invoke(() =>
                {
                    switch (status)
                    {
                        case ConnectionStatus.Success:
                            TopText = "Invite sent";
                            Task.Run(() =>
                            {
                                NetworkManager.handleConnection(NetworkManager.GetActiveClient());
                            });
                            break;
                        case ConnectionStatus.InviteDeclined:
                            TopText = "Invite declined.";
                            break;
                        case ConnectionStatus.NoServer:
                            TopText = "No active server on that port.";
                            break;
                        case ConnectionStatus.ConnectionLost:
                            TopText = "Connection lost.";
                            break;
                    }
                });
            });
        }



        public void sendMessage()
        {
            var message = new ChatMessage
            {
                Nickname = UserName,
                MessageText = MyText,
                Timestamp = DateTime.Now,
                Type = "chat"
            };

            NetworkManager.SendMessage(message.Nickname, message.MessageText, message.Type);

            string formattedMessage = $"{message.Timestamp} - {message.Nickname} \n{message.MessageText}";

            Application.Current.Dispatcher.Invoke(() =>
            {
                Messages.Add(formattedMessage);
                MyText = string.Empty;
            });
        }


        public void showChatWindow()
        {
            chatWindow = new ChatWindow();
            chatWindow.DataContext = this;
            LoadChatHistoryList();
            Application.Current.Dispatcher.Invoke(() =>
            {
                Application.Current.MainWindow.Visibility = Visibility.Hidden;
            });
            chatWindow.Closing += ChatWindow_Closing;
            chatWindow.Show();
            showButtons(false);
        }

        public void showButtons(bool b)
        {
            if (chatWindow == null) return;

            var visibility = b ? Visibility.Visible : Visibility.Collapsed;
            var enabled = b;

            AcceptButtonVisibility = visibility;
            DeclineButtonVisibility = visibility;
            AcceptButtonEnabled = enabled;
            DeclineButtonEnabled = enabled;
        }


        public void declineInvite()
        {
            NetworkManager.SendMessage(UserName, "decline", "response");
            Task.Delay(100).Wait();
            UpdateStatusText("");
            NetworkManager.Disconnect(null);
            NetworkManager.ActiveRequest = false;
            NetworkManager.IsConnected = false;
            showButtons(false);
        }
        public void acceptInvite()
        {
            NetworkManager.SendMessage(UserName, "accept", "response");
            showButtons(false);
            UpdateStatusText($"Chatting with {NetworkManager.ChatPeer}");
        }

        public void UpdateStatusText(string message)
        {
            StatusText = message;
        }

        public void AddMessageToHistory(string chatPeer, ChatMessage message)
        {
            if (string.IsNullOrEmpty(chatPeer))
            {
                chatPeer = NetworkManager.ChatPeer ?? UserName;
            }
            if (message.Type == "chat")
            {
                chatHistoryManager.AddMessage(chatPeer, message);
            }
            Application.Current.Dispatcher.Invoke(() =>
            {
                LoadChatHistoryList();
            });
        }


        public void LoadChatHistoryList()
        {
            ChatHistoryItems.Clear();

            // Filter the History dictionary based on the Messages property of ChatHistory
            var filteredHistory = chatHistoryManager.History
                .Where(h => h.Value.Messages.Any(m =>  // h.Value is the ChatHistory object
                    (m.Sender == UserName || m.Receiver == UserName) && m.Type == "chat"))
                .OrderByDescending(h => h.Value.LastMessageTime);  // h.Value to access ChatHistory

            foreach (var history in filteredHistory)
            {
                ChatHistoryItems.Add(history.Value);  // Add the ChatHistory object (h.Value) to the list
            }
        }





        public void LoadChatHistory(ChatHistory history)
        {
            if (history != null)
            {
                Messages.Clear();
                foreach (var message in history.Messages)
                {
                    Messages.Add($"{message.Timestamp} - {message.Nickname} \n{message.MessageText}");
                }
            }
        }

        public void SearchChatHistory(string query)
        {
            if (string.IsNullOrWhiteSpace(query))
            {
                LoadChatHistoryList();
                return;
            }

            var results = chatHistoryManager.History
                .Where(h => h.Value.ChatPeer != null && h.Value.ChatPeer.Contains(query, StringComparison.OrdinalIgnoreCase)) // h.Value to access ChatHistory
                .OrderByDescending(h => h.Value.LastMessageTime); // h.Value to access LastMessageTime

            ChatHistoryItems.Clear();
            foreach (var item in results)
            {
                ChatHistoryItems.Add(item.Value);  // Add the ChatHistory object (h.Value) to the collection
            }
        }


        public void SaveChatHistory()
        {
            chatHistoryManager.SaveHistory();
            Application.Current.Dispatcher.Invoke(() =>
            {
                TopText = "";
            });
        }

        public void updateTopText(string text)
        {
            Application.Current.Dispatcher.Invoke(() =>
            {
                TopText = text;
            });
        }

        public void SendBuzz()
        {
            NetworkManager.SendMessage(UserName, "Buzz!", "buzz");
        }

        public void PlayBuzzSound()
        {
            var player = new System.Media.SoundPlayer("buzz.wav");
            player.Play();
        }

        public void ShakeWindow()
        {
            var window = Application.Current.Windows.OfType<ChatWindow>().FirstOrDefault();

            if (window != null)
            {
                var originalLeft = window.Left;
                var originalTop = window.Top;

                var rnd = new Random();
                const int shake = 10;

                for (int i = 0; i < 10; i++)
                {
                    window.Left = originalLeft + rnd.Next(-shake, shake);
                    window.Top = originalTop + rnd.Next(-shake, shake);
                    Thread.Sleep(50);
                }

                window.Left = originalLeft;
                window.Top = originalTop;
            }
        }

        // deklarerade de här för att hantera UI relterade funktioner
        public void HandleReceivedMessage(string chatPeer, ChatMessage message)
        {
            Application.Current.Dispatcher.Invoke(() =>
            {
                AddMessageToHistory(chatPeer, message);
                Messages.Add($"{message.Timestamp} - {message.Nickname} \n{message.MessageText}");
            });
        }

        public void HandleSentMessage(string chatPeer, ChatMessage message)
        {
            Application.Current.Dispatcher.Invoke(() =>
            {
                AddMessageToHistory(chatPeer, message);
                Messages.Add($"{message.Timestamp} - {message.Nickname} \n{message.MessageText}");
                MyText = string.Empty;
            });
        }

        public void HandleBuzz()
        {
            Application.Current.Dispatcher.Invoke(() =>
            {
                PlayBuzzSound();
                ShakeWindow();
            });
        }
    }
}