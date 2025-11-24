using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace ChatApp.Model
{
   
        public class ChatHistoryManager
        {
            private const string HistoryFilePath = "ChatHistory.json";

            // Use a Dictionary to map ChatPeer to ChatHistory
            public Dictionary<string, ChatHistory> History { get; private set; } = new Dictionary<string, ChatHistory>();

            public ChatHistoryManager()
            {
                LoadHistory();
            }

            public void AddMessage(string chatPeer, ChatMessage message)
            {
                if (!History.TryGetValue(chatPeer, out var conversation))
                {
                    conversation = new ChatHistory { ChatPeer = chatPeer };
                    History[chatPeer] = conversation;  // Add or update the Dictionary
                }

                conversation.Messages.Add(message);
                conversation.LastMessageTime = message.Timestamp;

            }

            private readonly object fileLock = new object();

            public void SaveHistory()
            {
                lock (fileLock)
                {
                    var filteredHistory = History.Values
                        .Where(h => h.Messages.Any(m => m.Type == "chat"))
                        .ToList();

                    var json = System.Text.Json.JsonSerializer.Serialize(filteredHistory);
                    File.WriteAllText(HistoryFilePath, json);
                }
            }

            public void LoadHistory()
            {
                if (File.Exists(HistoryFilePath))
                {
                    var json = File.ReadAllText(HistoryFilePath);
                    if (string.IsNullOrWhiteSpace(json))
                    {
                        History = new Dictionary<string, ChatHistory>();
                        SaveHistory();
                        return;
                    }

                    try
                    {
                  
                        var loadedHistory = System.Text.Json.JsonSerializer.Deserialize<List<ChatHistory>>(json);
                        History = loadedHistory.ToDictionary(h => h.ChatPeer);
                    }
                    catch (System.Text.Json.JsonException)
                    {
                        History = new Dictionary<string, ChatHistory>();
                        SaveHistory();
                    }
                }
                else
                {
                    History = new Dictionary<string, ChatHistory>();
                }
            }

        public List<ChatHistory> SearchHistory(string searchText)
            {
                return History.Values
                    .Where(h => h.ChatPeer.Contains(searchText, StringComparison.OrdinalIgnoreCase))
                    .OrderByDescending(h => h.LastMessageTime)
                    .ToList();
            }
        }
    
}

