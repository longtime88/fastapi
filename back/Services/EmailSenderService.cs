using MailKit.Net.Smtp;
using MailKit.Security;
using Microsoft.Extensions.Configuration;
using MimeKit;

namespace SupportInbox.Services;

public class EmailSenderService
{
    private readonly IConfiguration _config;

    public EmailSenderService(IConfiguration config)
    {
        _config = config;
    }

    public async Task SendReplyAsync(string to, string subject, string body, string fromEmail, string fromName)
    {
        var smtpConfig = _config.GetSection("Smtp");
        var smtpHost = smtpConfig["Host"] ?? throw new InvalidOperationException("Smtp:Host is not configured");
        var smtpPort = int.Parse(smtpConfig["Port"] ?? "587");
        var smtpUser = smtpConfig["Username"] ?? "";
        var smtpPass = smtpConfig["Password"] ?? "";
        var enableSsl = bool.Parse(smtpConfig["EnableSsl"] ?? "true");

        var message = new MimeMessage();
        message.From.Add(new MailboxAddress(fromName, fromEmail));
        message.To.Add(MailboxAddress.Parse(to));
        message.Subject = subject;

        var bodyBuilder = new BodyBuilder
        {
            TextBody = StripHtml(body),
            HtmlBody = body
        };
        message.Body = bodyBuilder.ToMessageBody();

        using var client = new SmtpClient();
        var secOptions = enableSsl ? SecureSocketOptions.StartTls : SecureSocketOptions.None;
        await client.ConnectAsync(smtpHost, smtpPort, secOptions);
        await client.AuthenticateAsync(smtpUser, smtpPass);
        await client.SendAsync(message);
        await client.DisconnectAsync(true);
    }

    private static string StripHtml(string html)
    {
        return System.Text.RegularExpressions.Regex.Replace(html, "<[^>]*>", String.Empty);
    }

    public string GetSenderEmail()
    {
        return _config.GetSection("Smtp")["FromEmail"] ?? "";
    }

    public string GetSenderName()
    {
        return _config.GetSection("Smtp")["FromName"] ?? "";
    }
}