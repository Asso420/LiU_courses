
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using ChatApp.View;
using ChatApp.ViewModel;

namespace ChatApp.Model
{
    public enum ConnectionStatus
    {
        Success,
        InviteDeclined,
        NoServer,
        ConnectionLost
    }
    public class ChatMessage // 
    {
        public string Nickname { get; set; }
        public string MessageText { get; set; }
        public DateTime Timestamp { get; set; }
        public string Type { get; set; }

        public string Sender { get; set; }
        public string Receiver { get; set; }
    }
    internal class NetworkManager : INotifyPropertyChanged // the class is internal so it can only be accessed by classes in the same assembly
    {
        private MainWindowViewModel viewModel;

        public void Initialize(MainWindowViewModel mainViewModel)
        {
            viewModel = mainViewModel;
        }


        

        public event PropertyChangedEventHandler PropertyChanged; // event handler for property changes

        private void OnPropertyChanged(string propertyName = "") // method to raise the PropertyChanged event
        {
            if (PropertyChanged != null) 
            {
                PropertyChanged(this, new PropertyChangedEventArgs(propertyName)); // raise the PropertyChanged event with the provided property name 

            }
        }
        private NetworkStream stream; // NetworkStream object to read and write data across network connections 
        private string message; 
        private string status;
        private string toptext; 
        private bool isConnected; 
        private bool activeRequest; 
        private string chatPeer; 
        private TcpClient activeClient; 
        public string Message 
        { 
            get { return message; } 
            set { message = value; OnPropertyChanged("Message"); }
        }

        public string Status // 
        {
            get => status;
            set { status = value; OnPropertyChanged("status"); } // set the status value and raise the PropertyChanged event
        }

        public string Toptext
        {
            get => toptext;
            set
            {
                if (toptext != value)
                {
                    toptext = value;
                    OnPropertyChanged("toptext");
                }
            }
        }

        public bool IsConnected 
        {
            get => isConnected;
            set
            {
                if (isConnected != value)
                {
                    isConnected = value;
                    if (isConnected)
                    {
                        OnPropertyChanged("acceptInvite"); // raise the PropertyChanged event for the acceptInvite property
                    }
                    else
                    {
                        OnPropertyChanged("declineInvite");
                    }
                }
            }
        }

        public bool ActiveRequest 
        {
            get => activeRequest;
            set
            {
                activeRequest = value; OnPropertyChanged("activeRequest");
            }
        }

        
        public string ChatPeer
        {
            get => chatPeer; 
            set { chatPeer = value; OnPropertyChanged(ChatPeer); }
        }
        
        public TcpClient GetActiveClient() => activeClient;


        public bool startHost(string nick, int port, string ip) // method to start hosting a server
        {
            try
            {
                TcpListener testListener = new TcpListener(IPAddress.Parse(ip), port); 
                testListener.Start();
                testListener.Stop(); 

                Task.Run(() => 
                {
                    TcpListener server = new TcpListener(IPAddress.Parse(ip), port);
                    server.Start();
                    Toptext = $"Hosting server on port {port}.";  // set the top text
                    while (true) 
                    {
                        TcpClient client = server.AcceptTcpClient();  
                        Task.Run(() => handleConnection(client)); 
                    }
                });

                return true;
            }
            catch (SocketException) 
            {
                Toptext = $"Port {port} is already in use."; 
                return false;
            }
        }

        public ConnectionStatus startConnection(string nick, int port, string ip) 
        {
            activeClient = new TcpClient();  
            try
            {
                var ipEndPoint = new IPEndPoint(IPAddress.Parse(ip), port); 
                activeClient.ConnectAsync(ipEndPoint);
                stream = activeClient.GetStream(); 
                SendMessage(nick, "invite", "invite"); 
                ActiveRequest = true; 
                return handleInvite(activeClient); 
            }
            catch (SocketException)
            {
                Application.Current.Dispatcher.Invoke(() => { 
                    Toptext = "No active server on that port.";
                });
                return ConnectionStatus.NoServer; 
            }
        }


        public ConnectionStatus handleInvite(TcpClient client) 
        {
            try
            {
                stream = client.GetStream();  
                while (client.Connected) 
                {
                    byte[] buffer = new byte[1024];  
                    int bytesRead = stream.Read(buffer, 0, buffer.Length);
                    if (bytesRead > 0) 
                    {
                        string jsonMessage = Encoding.UTF8.GetString(buffer, 0, bytesRead); 
                        var chatMessage = System.Text.Json.JsonSerializer.Deserialize<ChatMessage>(jsonMessage); 
                        if (chatMessage != null) 
                        {
                            if (chatMessage.Type == "response") 
                            {
                                if (chatMessage.MessageText == "accept")
                                {
                                    IsConnected = true;
                                    ActiveRequest = false;
                                    ChatPeer = chatMessage.Nickname;
                                    Status = $"Chatting with {chatMessage.Nickname}";
                                    return ConnectionStatus.Success;
                                }
                                else if (chatMessage.MessageText == "decline")
                                {
                                    IsConnected = false;
                                    ActiveRequest = false;
                                    Disconnect(client);
                                    return ConnectionStatus.InviteDeclined;
                                }
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Status = "Connection lost.";
                Toptext = "Connection lost.";
                IsConnected = false;
                return ConnectionStatus.ConnectionLost;
            }
            finally
            {
                if (!client.Connected)
                {
                    Disconnect(client);
                    ActiveRequest = false;
                }
            }
            return ConnectionStatus.ConnectionLost;
        }



        public void handleConnection(TcpClient client) 
        {
            try
            {
                stream = client.GetStream();
                while (client.Connected)
                {
                    byte[] buffer = new byte[1024];
                    int bytesRead = stream.Read(buffer, 0, buffer.Length);
                    if (bytesRead > 0)
                    {
                        string jsonMessage = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                        var chatMessage = System.Text.Json.JsonSerializer.Deserialize<ChatMessage>(jsonMessage);
                        if (chatMessage != null)
                        {
                            switch (chatMessage.Type)
                            {
                                case "chat":
                                    Message = $"{chatMessage.Timestamp} - {chatMessage.Nickname} \n{chatMessage.MessageText}";
                                    chatMessage.Sender = chatMessage.Nickname;
                                    //Application.Current.Dispatcher.Invoke(() =>
                                    //{
                                    //    viewModel?.AddMessageToHistory(ChatPeer, chatMessage);
                                    //});
                                    viewModel?.HandleReceivedMessage(ChatPeer, chatMessage);
                                    break;

                                case "invite":
                                    ActiveRequest = true;
                                    Status = $"Invite received from {chatMessage.Nickname}";
                                    ChatPeer = chatMessage.Nickname;
                                    break;

                                case "disconnect":
                                    Status = $"{chatMessage.Nickname} has disconnected.";
                                    IsConnected = false;
                                    Disconnect(client);
                                    break;

                                case "buzz":
                                    try
                                    {
                                        //Application.Current.Dispatcher.Invoke(() =>
                                        //{
                                        //    viewModel?.PlayBuzzSound();
                                        //    viewModel?.ShakeWindow();
                                        //});
                                        viewModel?.HandleBuzz();
                                    }
                                    catch (Exception ex)
                                    {
                                        System.Diagnostics.Debug.WriteLine($"Error handling buzz");
                                    }
                                    break;

                                default:
                                    break;
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                IsConnected = false;
            }
            finally
            {
                if (!client.Connected)
                {
                    Disconnect(client);
                    ActiveRequest = false;
                }
            }
        }


        public void Disconnect(TcpClient client)
        {
            try
            {
                client?.Close();
                stream?.Close();
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Error closing connection");
            }
            finally
            {
                client = null;
                stream = null;
                viewModel?.SaveChatHistory();
            }
            ActiveRequest = false;
            IsConnected = false;
        }


        public void SendMessage(string nickname, string messageText, string type)
        {
            Task.Run(() =>
            {
                if (stream != null && stream.CanWrite)
                {
                    var chatMessage = new ChatMessage
                    {
                        Nickname = nickname,
                        Sender = nickname,
                        Receiver = ChatPeer,
                        MessageText = messageText,
                        Timestamp = DateTime.Now,
                        Type = type
                    };
                    string jsonMessage = System.Text.Json.JsonSerializer.Serialize(chatMessage);
                    byte[] buffer = Encoding.UTF8.GetBytes(jsonMessage);
                    stream.Write(buffer, 0, buffer.Length);

                    //Application.Current.Dispatcher.Invoke(() =>
                    //{
                    //    viewModel?.AddMessageToHistory(ChatPeer, chatMessage);
                    //});
                    viewModel?.HandleSentMessage(ChatPeer, chatMessage);
                }
            });
        }

        public void SendDisconnectMessage(string nickname)
        {
            SendMessage(nickname, "disconnect", "disconnect");
        }

        public void Stop()
        {
            if (stream != null && stream.CanWrite)
            {
                SendDisconnectMessage("");
            }
            Disconnect(null);
        }
    }
}
