using SupportInbox.Models;
using SupportInbox.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Configuration.AddJsonFile("appsettings.json", optional: false, reloadOnChange: true);

builder.Services.AddSingleton<EmailInboxService>();
builder.Services.AddSingleton<EmailSenderService>();

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.MapControllers();

app.MapGet("/inbox/tickets", async (EmailInboxService service) =>
{
    var tickets = await service.GetUnreadTicketsAsync();
    return Results.Ok(tickets);
})
.WithName("GetTickets");

app.MapGet("/inbox/tickets/read", async (EmailInboxService service) =>
{
    var tickets = await service.GetAllTicketsAsync();
    return Results.Ok(tickets);
})
.WithName("GetAllTickets");

app.MapGet("/inbox/tickets/{id}", async (EmailInboxService service, int id) =>
{
    var ticket = await service.GetTicketByIdAsync(id);
    if (ticket is null) return Results.NotFound();
    return Results.Ok(ticket);
})
.WithName("GetTicketById");

app.MapPost("/inbox/tickets/{id}/mark-read", async (EmailInboxService service, int id) =>
{
    await service.MarkReadAsync(id);
    return Results.Ok(new { id, status = "read" });
})
.WithName("MarkRead");

app.MapPost("/inbox/tickets/{id}/reply", async (EmailInboxService inboxService, EmailSenderService senderService, int id, ReplyRequest request) =>
{
    var ticket = await inboxService.GetTicketByIdAsync(id);
    if (ticket is null) return Results.NotFound();

    await senderService.SendReplyAsync(
        ticket.From,
        $"Re: {ticket.Subject}",
        request.Body,
        senderService.GetSenderEmail(),
        senderService.GetSenderName()
    );

    await inboxService.MarkReadAsync(id);
    return Results.Ok(new { id, status = "sent", message = "Antwort wurde erfolgreich versendet" });
})
.WithName("SendReply");

app.MapGet("/health", () => Results.Ok(new { status = "healthy" }));

app.Run();