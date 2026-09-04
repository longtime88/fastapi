namespace SupportInbox.Models;

public class SupportTicket
{
    public int Id { get; set; }
    public string Subject { get; set; } = "";
    public string From { get; set; } = "";
    public string FromName { get; set; } = "";
    public string Body { get; set; } = "";
    public string BodyPlain { get; set; } = "";
    public DateTime ReceivedAt { get; set; }
    public bool IsRead { get; set; }
    public string MessageId { get; set; } = "";
}