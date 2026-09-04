using MailKit.Net.Imap;
using MailKit.Search;
using MailKit;
using Microsoft.Extensions.Configuration;
using MimeKit;
using SupportInbox.Models;

namespace SupportInbox.Services;

public class EmailInboxService
{
    private readonly IConfiguration _config;
    private readonly List<SupportTicket> _tickets = new();
    private int _nextId = 1;

    public EmailInboxService(IConfiguration config)
    {
        _config = config;
    }

    public async Task<List<SupportTicket>> GetUnreadTicketsAsync()
    {
        await FetchEmailsAsync();
        return _tickets.Where(t => !t.IsRead).ToList();
    }

    public async Task<List<SupportTicket>> GetAllTicketsAsync()
    {
        await FetchEmailsAsync();
        return _tickets.ToList();
    }

    public async Task<SupportTicket?> GetTicketByIdAsync(int id)
    {
        await FetchEmailsAsync();
        return _tickets.FirstOrDefault(t => t.Id == id);
    }

    public async Task MarkReadAsync(int id)
    {
        var ticket = _tickets.FirstOrDefault(t => t.Id == id);
        if (ticket != null)
            ticket.IsRead = true;
    }

    private async Task FetchEmailsAsync()
    {
        if (_tickets.Count > 0) return;

        var imapConfig = _config.GetSection("Imap");
        var host = imapConfig["Host"] ?? throw new InvalidOperationException("Imap:Host is not configured");
        var port = int.Parse(imapConfig["Port"] ?? "993");
        var username = imapConfig["Username"] ?? "";
        var password = imapConfig["Password"] ?? "";
        var enableSsl = bool.Parse(imapConfig["EnableSsl"] ?? "true");

        using var client = new ImapClient();
        var secOptions = enableSsl ? SecureSocketOptions.SslOnConnect : SecureSocketOptions.StartTls;

        await client.ConnectAsync(host, port, secOptions);
        await client.AuthenticateAsync(username, password);

        var inbox = client.Inbox;
        await inbox.OpenAsync(FolderAccess.ReadOnly);

        var query = SearchQuery.NotSeen;
        var uids = inbox.Search(query);

        foreach (var uid in uids.Reverse())
        {
            var message = inbox.GetMessage(uid);
            var ticket = new SupportTicket
            {
                Id = _nextId++,
                Subject = message.Subject ?? "(no subject)",
                From = message.From.Mailboxes.FirstOrDefault()?.Address ?? "",
                FromName = message.From.Mailboxes.FirstOrDefault()?.Name ?? "",
                Body = message.HtmlBody ?? message.TextBody ?? "",
                BodyPlain = message.TextBody ?? "",
                ReceivedAt = message.Date.DateTime,
                IsRead = false,
                MessageId = message.MessageId,
            };
            _tickets.Add(ticket);
        }

        await client.DisconnectAsync(true);
    }
}