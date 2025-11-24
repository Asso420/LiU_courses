using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ChatApp.Model
{
    public class ChatHistory
    {
        public string ChatPeer { get; set; }
        public DateTime LastMessageTime { get; set; }
        public List<ChatMessage> Messages { get; set; } = new List<ChatMessage>();
        public Guid ConversationId { get; set; } = Guid.NewGuid();
    }
}
//fjkdfvjk