# Sample: MacroDeck.SampleRestApiPlugin

The `MacroDeck.SampleRestApiPlugin` sample plugin and its tests, one `## File: <path>` section per file. See `samples/README.md` for what each sample demonstrates.

Files:

- `src/MacroDeck.SampleRestApiPlugin/Actions/CompleteCardAction.cs`
- `src/MacroDeck.SampleRestApiPlugin/Actions/CreateCardAction.cs`
- `src/MacroDeck.SampleRestApiPlugin/Actions/RefreshBoardAction.cs`
- `src/MacroDeck.SampleRestApiPlugin/Actions/TaskBoardActionResults.cs`
- `src/MacroDeck.SampleRestApiPlugin/Api/TaskBoardClient.cs`
- `src/MacroDeck.SampleRestApiPlugin/Api/TaskBoardCredentials.cs`
- `src/MacroDeck.SampleRestApiPlugin/Api/TaskBoardException.cs`
- `src/MacroDeck.SampleRestApiPlugin/Api/TaskBoardModels.cs`
- `src/MacroDeck.SampleRestApiPlugin/Api/TaskBoardRegistration.cs`
- `src/MacroDeck.SampleRestApiPlugin/Assets/icon.svg`
- `src/MacroDeck.SampleRestApiPlugin/ConfigFlow/TaskBoardConfigFlow.cs`
- `src/MacroDeck.SampleRestApiPlugin/Localization/Strings.resx`
- `src/MacroDeck.SampleRestApiPlugin/MacroDeck.SampleRestApiPlugin.csproj`
- `src/MacroDeck.SampleRestApiPlugin/Program.cs`
- `src/MacroDeck.SampleRestApiPlugin/Properties/launchSettings.json`
- `src/MacroDeck.SampleRestApiPlugin/README.md`
- `src/MacroDeck.SampleRestApiPlugin/RestApiIntegration.cs`
- `src/MacroDeck.SampleRestApiPlugin/macrodeck-build.json`
- `src/MacroDeck.SampleRestApiPlugin/manifest.json`
- `tests/MacroDeck.SampleRestApiPlugin.Tests/FakeTaskBoardApi.cs`
- `tests/MacroDeck.SampleRestApiPlugin.Tests/LocalizationTests.cs`
- `tests/MacroDeck.SampleRestApiPlugin.Tests/MacroDeck.SampleRestApiPlugin.Tests.csproj`
- `tests/MacroDeck.SampleRestApiPlugin.Tests/TaskBoardConfigFlowTests.cs`
- `tests/MacroDeck.SampleRestApiPlugin.Tests/TaskBoardIntegrationTests.cs`

## File: src/MacroDeck.SampleRestApiPlugin/Actions/CompleteCardAction.cs

```csharp
using MacroDeck.Localization;
using MacroDeck.SampleRestApiPlugin.Api;
using MacroDeck.Sdk.Actions;

namespace MacroDeck.SampleRestApiPlugin.Actions;

/// <summary>
/// Changes remote state and then tells the rest of the plugin about it: the card list is re-read so
/// the variables agree with the server, and the event fires for anything listening.
/// </summary>
internal sealed class CompleteCardAction(RestApiIntegration integration)
	: IActionDefinition, IDynamicOptionsActionDefinition
{
	public string Id => "complete-card";

	public LocalizedText Name => Strings.Actions.CompleteCard.Name();

	public LocalizedText Description => Strings.Actions.CompleteCard.Description();

	public IReadOnlyList<ActionParameter> Parameters { get; } =
	[
		ActionParameter.DynamicChoice("cardId", label: Strings.Actions.CompleteCard.Card.Label(), required: true)
	];

	public IActionExecutor CreateExecutor() => new Executor(integration);

	/// <summary>A card's title is what the user wrote on the remote board, so the option label is a
	/// literal - there is nothing to translate about it.</summary>
	public async Task<DynamicOptionsResult> GetDynamicOptionsAsync(DynamicOptionsContext context, CancellationToken cancellationToken)
	{
		try
		{
			var cards = await integration.Client.GetCardsAsync(openOnly: true, cancellationToken);
			var matching = string.IsNullOrWhiteSpace(context.Filter)
				? cards
				: [.. cards.Where(card => card.Title.Contains(context.Filter, StringComparison.OrdinalIgnoreCase))];

			return new DynamicOptionsResult
			{
				Options = [.. matching.Select(card => new ActionParameterOption { Value = card.Id, Label = card.Title })]
			};
		}
		catch (TaskBoardException)
		{
			return new DynamicOptionsResult { Options = [] };
		}
	}

	private sealed class Executor(RestApiIntegration integration) : IActionExecutor
	{
		public async Task<ActionResult> ExecuteAsync(ActionExecutionContext context)
		{
			if (context.Parameters.GetValueOrDefault("cardId") is not string { Length: > 0 } cardId)
			{
				return ActionResult.Failed(ActionErrorCodes.InvalidParameter,
					MacroDeckStrings.Validation.Required(Strings.Actions.CompleteCard.Card.Label()));
			}

			try
			{
				var card = await integration.Client.CompleteCardAsync(cardId, context.CancellationToken);
				integration.PublishCardCompleted(card);
				await integration.RefreshAsync(context.CancellationToken);
				return ActionResult.Success();
			}
			catch (TaskBoardException exception)
			{
				return TaskBoardActionResults.From(exception);
			}
		}
	}
}
```

## File: src/MacroDeck.SampleRestApiPlugin/Actions/CreateCardAction.cs

```csharp
using MacroDeck.Localization;
using MacroDeck.SampleRestApiPlugin.Api;
using MacroDeck.Sdk.Actions;

namespace MacroDeck.SampleRestApiPlugin.Actions;

/// <summary>
/// The POST-shaped action: parameters become a request body, and the API's answer decides what the
/// action reports. Its list options come from the API itself, so the picker always shows the lists the
/// account really has.
/// </summary>
internal sealed class CreateCardAction(RestApiIntegration integration)
	: IActionDefinition, IDynamicOptionsActionDefinition
{
	private const string HighPriority = "high";

	public string Id => "create-card";

	public LocalizedText Name => Strings.Actions.CreateCard.Name();

	public LocalizedText Description => Strings.Actions.CreateCard.Description();

	public IReadOnlyList<ActionParameter> Parameters { get; } =
	[
		ActionParameter.Text("title", label: Strings.Actions.CreateCard.Title.Label(), required: true, maxLength: 120),
		ActionParameter.DynamicChoice("listId", label: Strings.Actions.CreateCard.List.Label(), required: true),
		// An option's Value is what the API is sent, so it stays as the API spells it; only the Label is
		// a reference the reader's client resolves.
		ActionParameter.Choice("priority",
			[
				new ActionParameterOption { Value = "low", Label = Strings.Priorities.Low() },
				new ActionParameterOption { Value = "normal", Label = Strings.Priorities.Normal() },
				new ActionParameterOption { Value = HighPriority, Label = Strings.Priorities.High() }
			],
			label: Strings.Actions.CreateCard.Priority.Label(),
			defaultValue: "normal"),
		ActionParameter.MultilineText("notes",
			label: Strings.Actions.CreateCard.Notes.Label(),
			placeholder: Strings.Actions.CreateCard.Notes.Placeholder()),
		// Only a high-priority card gets a due date in this workflow, so the field follows the choice.
		ActionParameter.DateTime("dueAt", label: Strings.Actions.CreateCard.DueAt.Label())
			.OnlyWhen("priority", HighPriority)
	];

	public IActionExecutor CreateExecutor() => new Executor(integration);

	public async Task<DynamicOptionsResult> GetDynamicOptionsAsync(DynamicOptionsContext context, CancellationToken cancellationToken)
	{
		try
		{
			var lists = await integration.Client.GetListsAsync(cancellationToken);
			return new DynamicOptionsResult
			{
				Options = [.. lists.Select(list => new ActionParameterOption { Value = list.Id, Label = list.Name })],
				CacheSeconds = 60
			};
		}
		catch (TaskBoardException)
		{
			// An empty list is the honest answer while the integration cannot reach its API; the issue
			// provider is what tells the user why.
			return new DynamicOptionsResult { Options = [] };
		}
	}

	private sealed class Executor(RestApiIntegration integration) : IActionExecutor
	{
		public async Task<ActionResult> ExecuteAsync(ActionExecutionContext context)
		{
			if (context.Parameters.GetValueOrDefault("title") is not string { Length: > 0 } title)
			{
				return ActionResult.Failed(ActionErrorCodes.InvalidParameter,
					MacroDeckStrings.Validation.Required(Strings.Actions.CreateCard.Title.Label()));
			}

			if (context.Parameters.GetValueOrDefault("listId") is not string { Length: > 0 } listId)
			{
				return ActionResult.Failed(ActionErrorCodes.InvalidParameter,
					MacroDeckStrings.Validation.Required(Strings.Actions.CreateCard.List.Label()));
			}

			var request = new CreateCardRequest(
				title,
				listId,
				context.Parameters.GetValueOrDefault("priority") as string ?? "normal",
				context.Parameters.GetValueOrDefault("notes") as string,
				context.Parameters.GetValueOrDefault("dueAt") is string due &&
					DateTimeOffset.TryParse(due, out var dueAt)
						? dueAt
						: null);

			try
			{
				// The token belongs to the invocation, not the plugin: a cancelled or timed-out call has
				// to stop the HTTP request too.
				await integration.Client.CreateCardAsync(request, context.CancellationToken);
				await integration.RefreshAsync(context.CancellationToken);
				return ActionResult.Success();
			}
			catch (TaskBoardException exception)
			{
				return TaskBoardActionResults.From(exception);
			}
		}
	}
}
```

## File: src/MacroDeck.SampleRestApiPlugin/Actions/RefreshBoardAction.cs

```csharp
using MacroDeck.Localization;
using MacroDeck.Sdk.Actions;

namespace MacroDeck.SampleRestApiPlugin.Actions;

/// <summary>The read-shaped action: re-reads the board so the variables catch up with the server.</summary>
internal sealed class RefreshBoardAction(RestApiIntegration integration) : IActionDefinition
{
	public string Id => "refresh-board";

	public LocalizedText Name => Strings.Actions.RefreshBoard.Name();

	public LocalizedText Description => Strings.Actions.RefreshBoard.Description();

	public IReadOnlyList<ActionParameter> Parameters { get; } = [];

	public IActionExecutor CreateExecutor() => new Executor(integration);

	private sealed class Executor(RestApiIntegration integration) : IActionExecutor
	{
		public async Task<ActionResult> ExecuteAsync(ActionExecutionContext context)
		{
			var failure = await integration.RefreshAsync(context.CancellationToken);
			return failure is null ? ActionResult.Success() : TaskBoardActionResults.From(failure);
		}
	}
}
```

## File: src/MacroDeck.SampleRestApiPlugin/Actions/TaskBoardActionResults.cs

```csharp
using MacroDeck.SampleRestApiPlugin.Api;
using MacroDeck.Sdk.Actions;

namespace MacroDeck.SampleRestApiPlugin.Actions;

/// <summary>
/// One place mapping an API failure onto a truthful <see cref="ActionResult"/>. The distinction
/// matters to the user: "not configured" points at the config flow, "unauthorized" at re-authenticating
/// and a timeout at retrying, and a generic failure would hide all three.
/// </summary>
internal static class TaskBoardActionResults
{
	/// <summary>Reports <see cref="TaskBoardException.UserMessage"/>, not <c>Message</c>: the error text
	/// reaches a client that resolves it in its own language, while the exception's own message stays
	/// what the log records.</summary>
	internal static ActionResult From(TaskBoardException exception) => ActionResult.Failed(exception.Reason switch
	{
		TaskBoardFailure.NotConfigured => ActionErrorCodes.NotConfigured,
		TaskBoardFailure.Unreachable => ActionErrorCodes.NotConnected,
		TaskBoardFailure.Timeout => ActionErrorCodes.Timeout,
		TaskBoardFailure.Unauthorized => ActionErrorCodes.PermissionDenied,
		TaskBoardFailure.NotFound => ActionErrorCodes.NotFound,
		_ => ActionErrorCodes.ProviderError
	}, exception.UserMessage);
}
```

## File: src/MacroDeck.SampleRestApiPlugin/Api/TaskBoardClient.cs

```csharp
using System.Net.Http.Headers;
using System.Net.Http.Json;

namespace MacroDeck.SampleRestApiPlugin.Api;

/// <summary>
/// The typed client, registered with <c>AddHttpClient&lt;TaskBoardClient&gt;()</c> so the handler
/// lifetime and connection pooling are the factory's problem rather than this class's. Everything a
/// caller can do to the remote service goes through here; nothing else in the plugin sees
/// <see cref="HttpClient"/>.
/// </summary>
public sealed class TaskBoardClient(HttpClient httpClient, TaskBoardCredentials credentials)
{
	public Task<IReadOnlyList<TaskBoardList>> GetListsAsync(CancellationToken cancellationToken)
		=> GetAsync<IReadOnlyList<TaskBoardList>>("lists", cancellationToken);

	public Task<IReadOnlyList<TaskBoardCard>> GetCardsAsync(bool openOnly, CancellationToken cancellationToken)
		=> GetAsync<IReadOnlyList<TaskBoardCard>>($"cards?open={(openOnly ? "true" : "false")}", cancellationToken);

	public async Task<TaskBoardCard> CreateCardAsync(CreateCardRequest request, CancellationToken cancellationToken)
	{
		using var message = CreateMessage(HttpMethod.Post, "cards");
		message.Content = JsonContent.Create(request);
		return await SendAsync<TaskBoardCard>(message, cancellationToken);
	}

	public async Task<TaskBoardCard> CompleteCardAsync(string cardId, CancellationToken cancellationToken)
	{
		using var message = CreateMessage(HttpMethod.Post, $"cards/{Uri.EscapeDataString(cardId)}/complete");
		return await SendAsync<TaskBoardCard>(message, cancellationToken);
	}

	/// <summary>A cheap round trip that tells "wrong token" apart from "service down". It takes the values
	/// explicitly so the config flow can check what a user just typed without applying it first.</summary>
	public async Task VerifyAsync(Uri baseAddress, string token, CancellationToken cancellationToken)
	{
		using var message = new HttpRequestMessage(HttpMethod.Get, new Uri(baseAddress, "lists"));
		message.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);
		using var response = await SendCoreAsync(message, cancellationToken);
	}

	/// <summary>The same check against the configured values, used by the issue provider.</summary>
	public async Task VerifyAsync(CancellationToken cancellationToken)
	{
		using var message = CreateMessage(HttpMethod.Get, "lists");
		using var response = await SendCoreAsync(message, cancellationToken);
	}

	private async Task<T> GetAsync<T>(string path, CancellationToken cancellationToken)
	{
		using var message = CreateMessage(HttpMethod.Get, path);
		return await SendAsync<T>(message, cancellationToken);
	}

	private async Task<T> SendAsync<T>(HttpRequestMessage message, CancellationToken cancellationToken)
	{
		using var response = await SendCoreAsync(message, cancellationToken);

		var payload = await response.Content.ReadFromJsonAsync<T>(cancellationToken);
		return payload ?? throw TaskBoardException.EmptyBody();
	}

	private async Task<HttpResponseMessage> SendCoreAsync(HttpRequestMessage message, CancellationToken cancellationToken)
	{
		HttpResponseMessage response;
		try
		{
			response = await httpClient.SendAsync(message, cancellationToken);
		}
		catch (TaskCanceledException exception) when (!cancellationToken.IsCancellationRequested)
		{
			// A cancelled request the caller did not cancel is the client's own timeout.
			throw TaskBoardException.Timeout(exception);
		}
		catch (HttpRequestException exception)
		{
			throw TaskBoardException.Unreachable(exception);
		}

		if (!response.IsSuccessStatusCode)
		{
			var failure = TaskBoardException.FromStatus(response.StatusCode);
			response.Dispose();
			throw failure;
		}

		return response;
	}

	private HttpRequestMessage CreateMessage(HttpMethod method, string path)
	{
		if (credentials is not { BaseAddress: { } baseAddress, Token: { } token })
		{
			throw TaskBoardException.NotConfigured();
		}

		var message = new HttpRequestMessage(method, new Uri(baseAddress, path));
		message.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);
		return message;
	}
}
```

## File: src/MacroDeck.SampleRestApiPlugin/Api/TaskBoardCredentials.cs

```csharp
namespace MacroDeck.SampleRestApiPlugin.Api;

/// <summary>
/// What the config flow produced, held as a singleton so the typed client can be registered before any
/// of it is known. A plugin is configured after it starts, so the base address and the token cannot be
/// baked into <c>AddHttpClient</c> at registration time.
/// </summary>
public sealed class TaskBoardCredentials
{
	private volatile Snapshot _current = new(null, null);

	public bool IsConfigured => _current is { BaseAddress: not null, Token: not null };

	public Uri? BaseAddress => _current.BaseAddress;

	public string? Token => _current.Token;

	public void Apply(Uri? baseAddress, string? token) => _current = new Snapshot(baseAddress, token);

	public void Clear() => _current = new Snapshot(null, null);

	private sealed record Snapshot(Uri? BaseAddress, string? Token);
}
```

## File: src/MacroDeck.SampleRestApiPlugin/Api/TaskBoardException.cs

```csharp
using System.Net;
using MacroDeck.Localization;

namespace MacroDeck.SampleRestApiPlugin.Api;

/// <summary>
/// One failure type for the whole client, carrying the reason callers actually branch on. Actions map
/// <see cref="Reason"/> onto an <c>ActionResult</c> error code and the issue provider maps it onto an
/// integration issue, so neither has to inspect HTTP status codes itself.
/// <para>
/// <see cref="Exception.Message"/> and <see cref="UserMessage"/> say the same thing twice on purpose:
/// the first is diagnostic text for the log, in one fixed language, and the second is the reference the
/// host resolves for whoever is reading the deck. Anything a user sees uses the second.
/// </para>
/// </summary>
public sealed class TaskBoardException : Exception
{
	public TaskBoardException(
		TaskBoardFailure reason,
		string message,
		LocalizedText userMessage,
		Exception? innerException = null)
		: base(message, innerException)
	{
		Reason = reason;
		UserMessage = userMessage;
	}

	public TaskBoardFailure Reason { get; }

	/// <summary>The same failure as text a client resolves in its own language.</summary>
	public LocalizedText UserMessage { get; }

	public static TaskBoardException NotConfigured() => new(
		TaskBoardFailure.NotConfigured,
		"The Task Board integration is not configured yet.",
		Strings.Failures.NotConfigured());

	public static TaskBoardException Unreachable(Exception innerException) => new(
		TaskBoardFailure.Unreachable,
		"The Task Board API is unreachable.",
		Strings.Failures.Unreachable(),
		innerException);

	public static TaskBoardException Timeout(Exception innerException) => new(
		TaskBoardFailure.Timeout,
		"The Task Board API did not answer in time.",
		Strings.Failures.Timeout(),
		innerException);

	public static TaskBoardException EmptyBody() => new(
		TaskBoardFailure.ServerError,
		"The Task Board API answered with an empty body.",
		Strings.Failures.EmptyBody());

	public static TaskBoardException FromStatus(HttpStatusCode status) => status switch
	{
		HttpStatusCode.Unauthorized or HttpStatusCode.Forbidden => new TaskBoardException(
			TaskBoardFailure.Unauthorized,
			"The Task Board API rejected the token.",
			Strings.Failures.Unauthorized()),
		HttpStatusCode.NotFound => new TaskBoardException(
			TaskBoardFailure.NotFound,
			"The Task Board API does not know that item.",
			Strings.Failures.NotFound()),
		_ => new TaskBoardException(
			TaskBoardFailure.ServerError,
			$"The Task Board API answered {(int)status}.",
			Strings.Failures.ServerError((int)status))
	};
}

public enum TaskBoardFailure
{
	NotConfigured,
	Unreachable,
	Timeout,
	Unauthorized,
	NotFound,
	ServerError
}
```

## File: src/MacroDeck.SampleRestApiPlugin/Api/TaskBoardModels.cs

```csharp
using System.Text.Json.Serialization;

namespace MacroDeck.SampleRestApiPlugin.Api;

/// <summary>The request and response bodies of the imaginary Task Board API this sample talks to.</summary>
public sealed record TaskBoardList(
	[property: JsonPropertyName("id")] string Id,
	[property: JsonPropertyName("name")] string Name);

public sealed record TaskBoardCard(
	[property: JsonPropertyName("id")] string Id,
	[property: JsonPropertyName("title")] string Title,
	[property: JsonPropertyName("listId")] string ListId,
	[property: JsonPropertyName("priority")] string Priority,
	[property: JsonPropertyName("done")] bool Done,
	[property: JsonPropertyName("dueAt")] DateTimeOffset? DueAt);

public sealed record CreateCardRequest(
	[property: JsonPropertyName("title")] string Title,
	[property: JsonPropertyName("listId")] string ListId,
	[property: JsonPropertyName("priority")] string Priority,
	[property: JsonPropertyName("notes")] string? Notes,
	[property: JsonPropertyName("dueAt")] DateTimeOffset? DueAt);
```

## File: src/MacroDeck.SampleRestApiPlugin/Api/TaskBoardRegistration.cs

```csharp
using Microsoft.Extensions.DependencyInjection;

namespace MacroDeck.SampleRestApiPlugin.Api;

/// <summary>
/// The client's registration, in one place so a test can start from the same wiring the plugin runs
/// with and only replace the primary handler.
/// </summary>
public static class TaskBoardRegistration
{
	public static IHttpClientBuilder AddTaskBoardApi(this IServiceCollection services)
	{
		services.AddSingleton<TaskBoardCredentials>();

		// No base address here: it is only known once the config flow has run, so every request builds
		// its own absolute URI from TaskBoardCredentials.
		return services.AddHttpClient<TaskBoardClient>(client => client.Timeout = TimeSpan.FromSeconds(10));
	}
}
```

## File: src/MacroDeck.SampleRestApiPlugin/Assets/icon.svg

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
	<rect x="10" y="12" width="44" height="40" rx="6" fill="#4A90D9" />
	<path d="M19 27h11M19 34h20M19 41h15" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" />
	<circle cx="45" cy="24" r="7" fill="#7ED321" />
</svg>
```

## File: src/MacroDeck.SampleRestApiPlugin/ConfigFlow/TaskBoardConfigFlow.cs

```csharp
using MacroDeck.Localization;
using MacroDeck.SampleRestApiPlugin.Api;
using MacroDeck.Sdk.Actions;
using MacroDeck.Sdk.ConfigFlow;

namespace MacroDeck.SampleRestApiPlugin.ConfigFlow;

/// <summary>
/// The realistic counterpart to the weather sample's one-field flow: several steps, a branch, a value
/// stored as a secret, and an external authorization round trip. What a step collects is verified
/// against the real API before the entry is completed, so a wrong token fails in the wizard rather
/// than as a broken integration afterwards.
/// </summary>
internal sealed class TaskBoardConfigFlow(TaskBoardClient client) : IConfigFlow
{
	internal const string ServerUrlKey = "serverUrl";
	internal const string TokenKey = "token";

	private const string ServerStepId = "server";
	private const string TokenStepId = "token";
	private const string CallbackStepId = "oauth-callback";

	private const string TokenAuth = "token";
	private const string OAuthAuth = "oauth";

	private Uri? _baseAddress;

	public Task<ConfigFlowResult> StartAsync(IConfigFlowContext context, CancellationToken cancellationToken)
		=> Task.FromResult(ConfigFlowResult.Step(ServerStep()));

	public async Task<ConfigFlowResult> SubmitAsync(
		string stepId,
		IReadOnlyDictionary<string, object?> input,
		IConfigFlowContext context,
		CancellationToken cancellationToken)
		=> stepId switch
		{
			ServerStepId => SubmitServer(input, context),
			TokenStepId => await SubmitTokenAsync(input, cancellationToken),
			CallbackStepId => await SubmitCallbackAsync(context, cancellationToken),
			_ => ConfigFlowResult.Error(ServerStep(), Strings.ConfigFlow.UnknownStep())
		};

	private ConfigFlowResult SubmitServer(IReadOnlyDictionary<string, object?> input, IConfigFlowContext context)
	{
		if (input.GetValueOrDefault(ServerUrlKey) is not string url ||
			!Uri.TryCreate(EnsureTrailingSlash(url), UriKind.Absolute, out var baseAddress) ||
			baseAddress.Scheme is not ("http" or "https"))
		{
			return ConfigFlowResult.Error(ServerStep(),
				MacroDeckStrings.Validation.InvalidUrl(Strings.ConfigFlow.Server.ServerUrl.Label()),
				new Dictionary<string, LocalizedText>
				{
					[ServerUrlKey] = Strings.ConfigFlow.Server.InvalidUrl()
				});
		}

		_baseAddress = baseAddress;

		if (input.GetValueOrDefault("authMethod") as string != OAuthAuth)
		{
			return ConfigFlowResult.Step(TokenStep());
		}

		// The host opens this URL, catches the redirect back to its own callback and resumes the flow at
		// ResumeStepId. RedirectUri and State come from the host, never from the plugin.
		var authorizeUrl = new UriBuilder(new Uri(baseAddress, "oauth/authorize"))
		{
			Query = $"response_type=code&client_id=macro-deck-sample" +
				$"&redirect_uri={Uri.EscapeDataString(context.OAuth.RedirectUri)}" +
				$"&state={Uri.EscapeDataString(context.OAuth.State)}"
		}.Uri;

		return ConfigFlowResult.External(authorizeUrl.ToString(), CallbackStepId);
	}

	private async Task<ConfigFlowResult> SubmitTokenAsync(
		IReadOnlyDictionary<string, object?> input,
		CancellationToken cancellationToken)
	{
		if (input.GetValueOrDefault(TokenKey) is not string { Length: > 0 } token)
		{
			var required = MacroDeckStrings.Validation.Required(Strings.ConfigFlow.Token.ApiToken.Label());

			return ConfigFlowResult.Error(TokenStep(),
				required,
				new Dictionary<string, LocalizedText> { [TokenKey] = required });
		}

		return await CompleteAsync(token, TokenStep(), cancellationToken);
	}

	private async Task<ConfigFlowResult> SubmitCallbackAsync(IConfigFlowContext context, CancellationToken cancellationToken)
	{
		// Over the wire the authorization code is passed as an argument on the call that carries it
		// rather than being a live value to poll - see capability-parity.md.
		if (context.OAuth.AuthorizationCode is not { Length: > 0 } code)
		{
			return ConfigFlowResult.Error(ServerStep(), Strings.ConfigFlow.OAuth.Cancelled());
		}

		// A real integration posts the code to the service's token endpoint here. The sample's imaginary
		// service accepts the code itself as a bearer token, so there is nothing to exchange.
		return await CompleteAsync(code, ServerStep(), cancellationToken);
	}

	private async Task<ConfigFlowResult> CompleteAsync(string token, ConfigFlowStep retryStep, CancellationToken cancellationToken)
	{
		if (_baseAddress is not { } baseAddress)
		{
			return ConfigFlowResult.Error(ServerStep(), Strings.ConfigFlow.Server.SessionLost());
		}

		try
		{
			await client.VerifyAsync(baseAddress, token, cancellationToken);
		}
		catch (TaskBoardException exception)
		{
			return ConfigFlowResult.Error(retryStep, exception.UserMessage);
		}

		// Values named here are persisted under those keys; the secret one lands in the host's secret
		// store and can only be read back through GetSecretAsync. The entry title is deliberately a plain
		// string: the host stores it as the entry's name and the user renames it from there.
		return ConfigFlowResult.Complete($"Task Board ({baseAddress.Host})", new Dictionary<string, ConfigFlowValue>
		{
			[ServerUrlKey] = ConfigFlowValue.Plain(baseAddress.ToString()),
			[TokenKey] = ConfigFlowValue.Secret(token)
		});
	}

	private static string EnsureTrailingSlash(string url)
		=> url.EndsWith('/') ? url : url + "/";

	private static ConfigFlowStep ServerStep() => new()
	{
		StepId = ServerStepId,
		Title = Strings.ConfigFlow.Server.Title(),
		Description = Strings.ConfigFlow.Server.Description(),
		Links =
		[
			new ConfigFlowLink
			{
				Label = Strings.ConfigFlow.Server.ApiDocumentation(),
				Url = "https://example.com/task-board/api"
			}
		],
		Fields =
		[
			// A placeholder showing the shape of a URL is an example, not a sentence: it stays a literal.
			ActionParameter.Url(ServerUrlKey,
				label: Strings.ConfigFlow.Server.ServerUrl.Label(),
				placeholder: "https://task-board.example.com/api/",
				required: true,
				autoPrefixHttps: true),
			ActionParameter.Choice("authMethod",
				[
					new ActionParameterOption { Value = TokenAuth, Label = Strings.AuthMethods.Token() },
					new ActionParameterOption { Value = OAuthAuth, Label = Strings.AuthMethods.OAuth() }
				],
				label: Strings.ConfigFlow.Server.AuthMethod.Label(),
				defaultValue: TokenAuth,
				required: true)
		]
	};

	private static ConfigFlowStep TokenStep() => new()
	{
		StepId = TokenStepId,
		Title = Strings.ConfigFlow.Token.Title(),
		Description = Strings.ConfigFlow.Token.Description(),
		Instructions = [new ConfigFlowInstruction { Text = Strings.ConfigFlow.Token.Instruction() }],
		Fields = [ActionParameter.Secret(TokenKey, label: Strings.ConfigFlow.Token.ApiToken.Label(), required: true)]
	};
}
```

## File: src/MacroDeck.SampleRestApiPlugin/Localization/Strings.resx

```xml
<?xml version="1.0" encoding="utf-8"?>
<root>
  <!-- The default-language file. Every translation is checked against it and the fallback chain ends
       here, so it is required even for a plugin that ships one language. Add a language by adding
       Localization/Strings.<culture>.resx beside it (Strings.de.resx, Strings.pt-BR.resx).
       A dotted key becomes a nested class: Actions.Foo.Name is Strings.Actions.Foo.Name(). -->
  <resheader name="resmimetype">
    <value>text/microsoft-resx</value>
  </resheader>
  <resheader name="version">
    <value>2.0</value>
  </resheader>
  <resheader name="reader">
    <value>System.Resources.ResXResourceReader, System.Windows.Forms, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089</value>
  </resheader>
  <resheader name="writer">
    <value>System.Resources.ResXResourceWriter, System.Windows.Forms, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089</value>
  </resheader>
  <data name="Actions.RefreshBoard.Name" xml:space="preserve">
    <value>Refresh board</value>
  </data>
  <data name="Actions.RefreshBoard.Description" xml:space="preserve">
    <value>Re-reads the open cards from the Task Board.</value>
  </data>
  <data name="Actions.CreateCard.Name" xml:space="preserve">
    <value>Create card</value>
  </data>
  <data name="Actions.CreateCard.Description" xml:space="preserve">
    <value>Creates a card on the Task Board.</value>
  </data>
  <data name="Actions.CreateCard.Title.Label" xml:space="preserve">
    <value>Title</value>
  </data>
  <data name="Actions.CreateCard.List.Label" xml:space="preserve">
    <value>List</value>
  </data>
  <data name="Actions.CreateCard.Priority.Label" xml:space="preserve">
    <value>Priority</value>
  </data>
  <data name="Actions.CreateCard.Notes.Label" xml:space="preserve">
    <value>Notes</value>
  </data>
  <data name="Actions.CreateCard.Notes.Placeholder" xml:space="preserve">
    <value>Optional details</value>
  </data>
  <data name="Actions.CreateCard.DueAt.Label" xml:space="preserve">
    <value>Due</value>
  </data>
  <data name="Priorities.Low" xml:space="preserve">
    <value>Low</value>
  </data>
  <data name="Priorities.Normal" xml:space="preserve">
    <value>Normal</value>
  </data>
  <data name="Priorities.High" xml:space="preserve">
    <value>High</value>
  </data>
  <data name="Actions.CompleteCard.Name" xml:space="preserve">
    <value>Complete card</value>
  </data>
  <data name="Actions.CompleteCard.Description" xml:space="preserve">
    <value>Marks a card on the Task Board as done.</value>
  </data>
  <data name="Actions.CompleteCard.Card.Label" xml:space="preserve">
    <value>Card</value>
  </data>
  <data name="Events.CardCompleted.Name" xml:space="preserve">
    <value>Card completed</value>
  </data>
  <data name="Events.CardCompleted.Description" xml:space="preserve">
    <value>Raised when this integration completes a card on the Task Board.</value>
  </data>
  <data name="Events.CardCompleted.CardId.Label" xml:space="preserve">
    <value>Card id</value>
  </data>
  <data name="Events.CardCompleted.Title.Label" xml:space="preserve">
    <value>Title</value>
  </data>
  <data name="ConfigFlow.Server.Title" xml:space="preserve">
    <value>Task Board server</value>
  </data>
  <data name="ConfigFlow.Server.Description" xml:space="preserve">
    <value>Where the sample's imaginary Task Board API runs, and how to authenticate against it.</value>
  </data>
  <data name="ConfigFlow.Server.ApiDocumentation" xml:space="preserve">
    <value>API documentation</value>
  </data>
  <data name="ConfigFlow.Server.ServerUrl.Label" xml:space="preserve">
    <value>Server URL</value>
  </data>
  <data name="ConfigFlow.Server.AuthMethod.Label" xml:space="preserve">
    <value>Authentication</value>
  </data>
  <data name="ConfigFlow.Server.InvalidUrl" xml:space="preserve">
    <value>Must be an http(s) URL.</value>
  </data>
  <data name="ConfigFlow.Server.SessionLost" xml:space="preserve">
    <value>Start again: the server URL was lost with the session.</value>
  </data>
  <data name="AuthMethods.Token" xml:space="preserve">
    <value>API token</value>
  </data>
  <data name="AuthMethods.OAuth" xml:space="preserve">
    <value>Sign in (OAuth)</value>
  </data>
  <data name="ConfigFlow.Token.Title" xml:space="preserve">
    <value>API token</value>
  </data>
  <data name="ConfigFlow.Token.Description" xml:space="preserve">
    <value>Paste a personal API token. It is stored in the host's secret store, not in plain configuration.</value>
  </data>
  <data name="ConfigFlow.Token.Instruction" xml:space="preserve">
    <value>Open Task Board → Settings → API tokens and create a token with board access.</value>
  </data>
  <data name="ConfigFlow.Token.ApiToken.Label" xml:space="preserve">
    <value>API token</value>
  </data>
  <data name="ConfigFlow.OAuth.Cancelled" xml:space="preserve">
    <value>The authorization was cancelled or returned no code.</value>
  </data>
  <data name="ConfigFlow.UnknownStep" xml:space="preserve">
    <value>Unknown step.</value>
  </data>
  <data name="Issues.NotConfigured.Title" xml:space="preserve">
    <value>Task Board is not configured</value>
  </data>
  <data name="Issues.NotConfigured.Description" xml:space="preserve">
    <value>Add the server URL and a token to start using the integration.</value>
  </data>
  <data name="Issues.NotConfigured.Action" xml:space="preserve">
    <value>Configure</value>
  </data>
  <data name="Issues.Unauthorized.Title" xml:space="preserve">
    <value>The Task Board token is no longer valid</value>
  </data>
  <data name="Issues.Unauthorized.Description" xml:space="preserve">
    <value>The server rejected the stored token. Sign in again to replace it.</value>
  </data>
  <data name="Issues.Unauthorized.Action" xml:space="preserve">
    <value>Sign in again</value>
  </data>
  <data name="Issues.Unreachable.Title" xml:space="preserve">
    <value>The Task Board server did not answer</value>
  </data>
  <data name="Issues.Unreachable.Action" xml:space="preserve">
    <value>Retry</value>
  </data>
  <data name="Issues.Unreachable.Resolved" xml:space="preserve">
    <value>The Task Board server answered again.</value>
  </data>
  <data name="Issues.Unknown" xml:space="preserve">
    <value>Unknown issue {issueId}.</value>
  </data>
  <data name="Notifications.Unavailable.Title" xml:space="preserve">
    <value>Task Board unavailable</value>
  </data>
  <data name="Failures.NotConfigured" xml:space="preserve">
    <value>The Task Board integration is not configured yet.</value>
  </data>
  <data name="Failures.Unreachable" xml:space="preserve">
    <value>The Task Board API is unreachable.</value>
  </data>
  <data name="Failures.Timeout" xml:space="preserve">
    <value>The Task Board API did not answer in time.</value>
  </data>
  <data name="Failures.Unauthorized" xml:space="preserve">
    <value>The Task Board API rejected the token.</value>
  </data>
  <data name="Failures.NotFound" xml:space="preserve">
    <value>The Task Board API does not know that item.</value>
  </data>
  <data name="Failures.ServerError" xml:space="preserve">
    <value>The Task Board API answered {status}.</value>
    <comment>[status:int] The HTTP status code the API returned.</comment>
  </data>
  <data name="Failures.EmptyBody" xml:space="preserve">
    <value>The Task Board API answered with an empty body.</value>
  </data>
</root>
```

## File: src/MacroDeck.SampleRestApiPlugin/MacroDeck.SampleRestApiPlugin.csproj

```xml
<Project Sdk="Microsoft.NET.Sdk">

    <PropertyGroup>
        <OutputType>Exe</OutputType>
        <IsPackable>false</IsPackable>
        <UserSecretsId>MacroDeck.SampleRestApiPlugin-PluginDevelopment</UserSecretsId>
    </PropertyGroup>

    <!-- Microsoft.NET.Sdk plus this framework reference, not Microsoft.NET.Sdk.Web: a plugin is a
         headless process, and the framework reference is what supplies the hosting surface
         MacroDeck.Plugin.Hosting builds on. -->
    <ItemGroup>
        <FrameworkReference Include="Microsoft.AspNetCore.App" />
    </ItemGroup>

    <ItemGroup>
        <!-- Build-time only: compile-time diagnostics for plugin authors, the [MacroDeckSdkUsage]
             attribute the host reads to report real deprecation usage, and the source generator that
             turns Localization/*.resx into the typed Strings class. Never shipped in the output. -->
        <PackageReference Include="MacroDeck.Plugin.Analyzers" PrivateAssets="all" />
        <!-- Referenced directly rather than relied on transitively through the SDK: LocalizedText and
             the generated Strings class are part of this project's own source. -->
        <PackageReference Include="MacroDeck.Localization" />
        <PackageReference Include="MacroDeck.Plugin.Hosting" />
        <PackageReference Include="MacroDeck.Plugin.Serilog" />
        <PackageReference Include="MacroDeck.Sdk" />
    </ItemGroup>

    <!-- The SDK reads the manifest from the content root at startup and resolves the icon path against
         that same root, so both have to land next to the built executable. -->
    <ItemGroup>
        <Content Include="manifest.json" CopyToOutputDirectory="PreserveNewest" />
        <Content Include="Assets\icon.svg" CopyToOutputDirectory="PreserveNewest" />
    </ItemGroup>

</Project>
```

## File: src/MacroDeck.SampleRestApiPlugin/Program.cs

```csharp
using MacroDeck.Plugin.Hosting;
using MacroDeck.Plugin.Serilog;
using MacroDeck.SampleRestApiPlugin;
using MacroDeck.SampleRestApiPlugin.Api;

// Identity, description and icon are not set here: they come from manifest.json at the content root.
// Strings is generated from Localization/*.resx, so UseLocalization is what makes every LocalizedText
// this plugin hands the host resolve in the reader's language rather than falling back to its key.
var builder = MacroDeckPlugin.CreatePlugin(args)
	.UseMacroDeckLogging()
	.UseLocalization(Strings.LocalizationCatalog)
	.RegisterIntegration<RestApiIntegration>();

// The typed client is an ordinary IHttpClientFactory registration - a plugin is a normal .NET host, so
// nothing about DI changes here.
builder.Services.AddTaskBoardApi();

var plugin = builder.Build();

await plugin.RunAsync();
```

## File: src/MacroDeck.SampleRestApiPlugin/Properties/launchSettings.json

```json
{
  "$schema": "https://json.schemastore.org/launchsettings.json",
  "profiles": {
    "Macro Deck - Real Host": {
      "commandName": "Project",
      "dotnetRunMessages": true,
      "launchBrowser": false,
      "workingDirectory": "$(ProjectDir)",
      "environmentVariables": {
        "DOTNET_ENVIRONMENT": "Development",
        "MACRO_DECK_PLUGIN_MODE": "SelfRegistering",
        "MACRO_DECK_PLUGIN_HOST_URL": "http://127.0.0.1:8193",
        "MACRO_DECK_PLUGIN_STATE_DIRECTORY": ".macrodeck-dev-state"
      }
    }
  }
}
```

## File: src/MacroDeck.SampleRestApiPlugin/README.md

````markdown
# Sample Task Board plugin

How to build an integration for a third-party service: a typed HTTP client behind
`IHttpClientFactory`, credentials that arrive from a config flow, and honest failure reporting. The
service itself - a "Task Board" with lists and cards - is imaginary, but the plugin is shaped exactly
like one talking to a real API.

This is deliberately not another generic HTTP integration. It shows how *a specific service* is
integrated, not how to send arbitrary requests.

## Read these first

- **`Api/TaskBoardClient.cs`** - the typed client, registered with `AddHttpClient<TaskBoardClient>()`.
  Everything the plugin can do to the service goes through here; nothing else sees `HttpClient`.
- **`Api/TaskBoardException.cs`** - one failure type carrying the reason callers branch on, so neither
  the actions nor the issue provider inspect status codes themselves.
- **`Api/TaskBoardCredentials.cs`** - what the config flow produced. A plugin is configured *after* it
  starts, so the base address and the token cannot be baked into the registration.
- **`ConfigFlow/TaskBoardConfigFlow.cs`** - several steps, a branch, a value stored as a secret and an
  external OAuth round trip. What a step collects is verified against the API before the entry is
  completed, so a wrong token fails in the wizard rather than as a broken integration afterwards.
- **`RestApiIntegration.cs`** - reads the entry back in `InitializeAsync` (which the host re-runs when
  the configuration changes), keeps the variables in sync, and reports integration issues.
- **`Actions/TaskBoardActionResults.cs`** - the failure mapping. "Not configured", "token rejected" and
  "server unreachable" point the user at three different fixes, and a generic failure would hide all
  three.

## Integration issues

`GetIssuesAsync` is a live round trip, never a cached list - a stale issue is worse than none. The
three it can report are the three a user can actually act on, and two of them hand the user back to
the config flow through `IssueResolutionFollowUp.StartConfigFlow`.
- **`Localization/Strings.resx`** - every string a user reads, including one `Failures.*` entry per
  `TaskBoardFailure`. `TaskBoardException` carries both: `Message` for the log, in one fixed language,
  and `UserMessage` as the reference a client resolves for whoever is reading the deck.

## Running it against a local host

Use this project's **Macro Deck - Real Host** launch profile as described in the repository's
[run and debug guide](../../README.md#run-and-debug-against-macro-deck). There is no server to point it
at, which is itself the interesting part: without configuration the plugin reports the "not
configured" issue, and with a URL that does not answer it reports the unreachable one. To see the
happy path, run the tests - they include a fake server.

## Testing it

```bash
dotnet test tests/MacroDeck.SampleRestApiPlugin.Tests
```

`FakeTaskBoardApi.cs` is a deterministic stand-in plugged in as the client's primary handler, so the
plugin's own request building, JSON parsing and error mapping all still run for real.
`TaskBoardConfigFlowTests` drives the wizard step by step, including the OAuth branch.

## Packaging it

`macrodeck-build.json` names one self-contained `dotnet publish` per platform, and the manifest's
entrypoints name what that publish actually produces:

```bash
macrodeck-plugin build --output ./artifacts
```

```bash
macrodeck-plugin validate --artifact ./artifacts/app.macro-deck.sample-rest-api-1.0.0.macroDeckPlugin --level Publication
```
````

## File: src/MacroDeck.SampleRestApiPlugin/RestApiIntegration.cs

```csharp
using MacroDeck.Localization;
using MacroDeck.SampleRestApiPlugin.Actions;
using MacroDeck.SampleRestApiPlugin.Api;
using MacroDeck.SampleRestApiPlugin.ConfigFlow;
using MacroDeck.Sdk;
using MacroDeck.Sdk.Actions;
using MacroDeck.Sdk.ConfigFlow;
using MacroDeck.Sdk.Events;
using MacroDeck.Sdk.Issues;
using MacroDeck.Sdk.Notifications;
using MacroDeck.Sdk.Variables;
using Serilog;

namespace MacroDeck.SampleRestApiPlugin;

/// <summary>
/// How a plugin for a third-party service is put together: a typed client behind
/// <see cref="IHttpClientFactory"/>, credentials that arrive from a config flow, variables and events
/// fed by API state, and integration issues for the problems a user can actually fix.
/// </summary>
public sealed class RestApiIntegration : IPluginIntegration, IVariableProvider, IEventProvider,
	IConfigFlowProvider, IIntegrationIssueProvider
{
	internal const string CardCompletedEventId = "card-completed";

	private const string NotConfiguredIssueId = "not-configured";
	private const string UnauthorizedIssueId = "unauthorized";
	private const string UnreachableIssueId = "unreachable";

	private const string FailureNotificationKey = "task-board-failure";

	private readonly TaskBoardClient _client;
	private readonly TaskBoardCredentials _credentials;
	private readonly ILogger _logger;

	private IIntegrationContext? _context;
	private IReadOnlyList<TaskBoardCard> _openCards = [];

	public RestApiIntegration(TaskBoardClient client, TaskBoardCredentials credentials, ILogger logger)
	{
		_client = client;
		_credentials = credentials;
		_logger = logger.ForContext<RestApiIntegration>();
		Actions = [new RefreshBoardAction(this), new CreateCardAction(this), new CompleteCardAction(this)];
	}

	public IReadOnlyList<IActionDefinition> Actions { get; }

	public async Task InitializeAsync(IIntegrationContext context)
	{
		_context = context;

		// Runs again whenever the host reports the configuration changed, so applying the entry here
		// rather than in the flow is what makes reconfiguration take effect without a restart.
		var entries = await context.Config.GetEntriesAsync();
		if (entries.Count == 0)
		{
			_credentials.Clear();
			_logger.Information("Waiting for configuration.");
			return;
		}

		var entryId = entries[0].Id;
		var serverUrl = await context.Config.GetStringAsync(entryId, TaskBoardConfigFlow.ServerUrlKey);
		var token = await context.Config.GetSecretAsync(entryId, TaskBoardConfigFlow.TokenKey);

		_credentials.Apply(
			Uri.TryCreate(serverUrl, UriKind.Absolute, out var baseAddress) ? baseAddress : null,
			token);

		await RefreshAsync(CancellationToken.None);
	}

	public Task ShutdownAsync()
	{
		_context = null;
		_credentials.Clear();
		return Task.CompletedTask;
	}

	internal TaskBoardClient Client => _client;

	internal IReadOnlyList<TaskBoardCard> OpenCards => _openCards;

	/// <summary>Re-reads the board and reports the outcome once, through a keyed notification that
	/// replaces the previous one instead of stacking up. Returns the failure so a caller can report the
	/// real reason rather than inventing one.</summary>
	internal async Task<TaskBoardException?> RefreshAsync(CancellationToken cancellationToken)
	{
		try
		{
			_openCards = await _client.GetCardsAsync(openOnly: true, cancellationToken);
			_context?.Notifications.Dismiss(FailureNotificationKey);
			return null;
		}
		catch (TaskBoardException exception)
		{
			_openCards = [];
			_logger.Warning(exception, "Reading the board failed ({Reason}).", exception.Reason);

			if (exception.Reason != TaskBoardFailure.NotConfigured)
			{
				// UserNotificationRequest types both fields as plain strings, so this one notification stays
				// in the plugin's own language until the contract carries a reference.
				_context?.Notifications.Notify(new UserNotificationRequest
				{
					Title = "Task Board unavailable",
					Message = exception.Message,
					Level = UserNotificationLevel.Warning,
					Key = FailureNotificationKey
				});
			}

			return exception;
		}
	}

	internal void PublishCardCompleted(TaskBoardCard card)
		=> _context?.Events.Publish(CardCompletedEventId, new Dictionary<string, object?>
		{
			["cardId"] = card.Id,
			["title"] = card.Title
		});

	public IReadOnlyList<VariableDefinition> Variables { get; } =
	[
		VariableDefinition.Eager("sample_taskboard_open_cards", VariableType.Numeric, refreshInterval: TimeSpan.FromMinutes(1))
			with { Id = "open-cards" },
		VariableDefinition.Eager("sample_taskboard_next_card", VariableType.Text) with { Id = "next-card" },
		VariableDefinition.Eager("sample_taskboard_configured", VariableType.Boolean) with { Id = "configured" }
	];

	/// <summary>Every value here is unconfigured until the flow has run: <see cref="VariableReading.Unavailable"/>
	/// is how a provider says so, which the host renders as an empty value rather than a zero.</summary>
	public ValueTask<VariableReading> ReadAsync(string localId, CancellationToken cancellationToken = default)
		=> ValueTask.FromResult(localId switch
		{
			"configured" => VariableReading.Of(_credentials.IsConfigured),
			_ when !_credentials.IsConfigured => VariableReading.Unavailable,
			"open-cards" => VariableReading.Of(_openCards.Count),
			"next-card" when _openCards.Count > 0 => VariableReading.Of(_openCards[0].Title),
			_ => VariableReading.Unavailable
		});

	public IReadOnlyList<EventDefinition> EventDefinitions { get; } =
	[
		new EventDefinition
		{
			Id = CardCompletedEventId,
			Name = Strings.Events.CardCompleted.Name(),
			Description = Strings.Events.CardCompleted.Description(),
			PayloadParameters =
			[
				ActionParameter.Text("cardId", Strings.Events.CardCompleted.CardId.Label()),
				ActionParameter.Text("title", Strings.Events.CardCompleted.Title.Label())
			]
		}
	];

	public IConfigFlow CreateConfigFlow() => new TaskBoardConfigFlow(_client);

	public bool AllowsMultipleConfigurations => false;

	/// <summary>
	/// The problems a user can act on, checked live rather than cached - a stale issue list is worse
	/// than none. A healthy integration returns an empty list.
	/// </summary>
	public async Task<IReadOnlyList<IntegrationIssue>> GetIssuesAsync(CancellationToken cancellationToken = default)
	{
		if (!_credentials.IsConfigured)
		{
			return
			[
				new IntegrationIssue
				{
					Id = NotConfiguredIssueId,
					Title = Strings.Issues.NotConfigured.Title(),
					Description = Strings.Issues.NotConfigured.Description(),
					Severity = IntegrationIssueSeverity.Error,
					ActionLabel = Strings.Issues.NotConfigured.Action()
				}
			];
		}

		try
		{
			await _client.VerifyAsync(cancellationToken);
			return [];
		}
		catch (TaskBoardException exception) when (exception.Reason == TaskBoardFailure.Unauthorized)
		{
			return
			[
				new IntegrationIssue
				{
					Id = UnauthorizedIssueId,
					Title = Strings.Issues.Unauthorized.Title(),
					Description = Strings.Issues.Unauthorized.Description(),
					Severity = IntegrationIssueSeverity.Error,
					ActionLabel = Strings.Issues.Unauthorized.Action()
				}
			];
		}
		catch (TaskBoardException exception)
		{
			return
			[
				new IntegrationIssue
				{
					Id = UnreachableIssueId,
					Title = Strings.Issues.Unreachable.Title(),
					Description = exception.UserMessage,
					Severity = IntegrationIssueSeverity.Warning,
					ActionLabel = Strings.Issues.Unreachable.Action()
				}
			];
		}
	}

	/// <summary>
	/// What pressing an issue's action does. Two of these hand the user back to the config flow, which
	/// is the only thing that can actually fix them; the third just retries.
	/// </summary>
	public async Task<IssueResolution> ResolveIssueAsync(string issueId, CancellationToken cancellationToken = default)
	{
		switch (issueId)
		{
			case NotConfiguredIssueId:
			case UnauthorizedIssueId:
				return IssueResolution.Ok(followUp: IssueResolutionFollowUp.StartConfigFlow);

			case UnreachableIssueId:
				var failure = await RefreshAsync(cancellationToken);
				return failure is null
					? IssueResolution.Ok(Strings.Issues.Unreachable.Resolved())
					: IssueResolution.Failed(failure.UserMessage);

			default:
				return IssueResolution.Failed(Strings.Issues.Unknown(issueId));
		}
	}
}
```

## File: src/MacroDeck.SampleRestApiPlugin/macrodeck-build.json

```json
{
  "version": 1,
  "targets": {
    "win-x64": {
      "executable": "dotnet",
      "arguments": [
        "publish",
        "MacroDeck.SampleRestApiPlugin.csproj",
        "-c",
        "Release",
        "-r",
        "win-x64",
        "--self-contained",
        "true",
        "-o",
        "bin/publish/win-x64"
      ],
      "output": "bin/publish/win-x64"
    },
    "osx-arm64": {
      "executable": "dotnet",
      "arguments": [
        "publish",
        "MacroDeck.SampleRestApiPlugin.csproj",
        "-c",
        "Release",
        "-r",
        "osx-arm64",
        "--self-contained",
        "true",
        "-o",
        "bin/publish/osx-arm64"
      ],
      "output": "bin/publish/osx-arm64"
    },
    "osx-x64": {
      "executable": "dotnet",
      "arguments": [
        "publish",
        "MacroDeck.SampleRestApiPlugin.csproj",
        "-c",
        "Release",
        "-r",
        "osx-x64",
        "--self-contained",
        "true",
        "-o",
        "bin/publish/osx-x64"
      ],
      "output": "bin/publish/osx-x64"
    },
    "linux-x64": {
      "executable": "dotnet",
      "arguments": [
        "publish",
        "MacroDeck.SampleRestApiPlugin.csproj",
        "-c",
        "Release",
        "-r",
        "linux-x64",
        "--self-contained",
        "true",
        "-o",
        "bin/publish/linux-x64"
      ],
      "output": "bin/publish/linux-x64"
    }
  }
}
```

## File: src/MacroDeck.SampleRestApiPlugin/manifest.json

```json
{
  "$schema": "https://schemas.macro-deck.app/plugin-manifest-v1.schema.json",
  "manifestVersion": 1,
  "id": "app.macro-deck.sample-rest-api",
  "name": "Sample Task Board",
  "version": "1.0.0",
  "description": "How to integrate a third-party REST API: typed HttpClient through DI, a multi-step config flow with a secret and an OAuth branch, integration issues, API-backed variables, events and dynamic options.",
  "icon": "Assets/icon.svg",
  "entrypoints": {
    "win-x64": {
      "executable": "runtimes/win-x64/MacroDeck.SampleRestApiPlugin.exe"
    },
    "osx-arm64": {
      "executable": "runtimes/osx-arm64/MacroDeck.SampleRestApiPlugin"
    },
    "osx-x64": {
      "executable": "runtimes/osx-x64/MacroDeck.SampleRestApiPlugin"
    },
    "linux-x64": {
      "executable": "runtimes/linux-x64/MacroDeck.SampleRestApiPlugin"
    }
  },
  "publisher": {
    "name": "Macro Deck",
    "id": "app.macro-deck",
    "url": "https://macro-deck.app"
  },
  "license": "MIT",
  "homepage": "https://docs.macro-deck.app/introduction/samples-and-template/",
  "repository": "https://github.com/Macro-Deck-App/Macro-Deck-Sample-Plugins",
  "compatibility": {
    "macroDeck": ">=3.0.0-0"
  },
  "permissions": [
    "host:config",
    "host:variables",
    "events:publish",
    "net:outbound"
  ]
}
```

## File: tests/MacroDeck.SampleRestApiPlugin.Tests/FakeTaskBoardApi.cs

```csharp
using System.Net;
using System.Net.Http.Json;
using MacroDeck.SampleRestApiPlugin.Api;

namespace MacroDeck.SampleRestApiPlugin.Tests;

/// <summary>
/// A deterministic stand-in for the imaginary Task Board service, plugged in as the typed client's
/// primary handler. The plugin's own code is unchanged by this: it still builds real requests and
/// parses real JSON, which is what makes these tests worth more than mocking the client away.
/// </summary>
internal sealed class FakeTaskBoardApi : HttpMessageHandler
{
	internal const string ValidToken = "valid-token";
	internal static readonly Uri BaseAddress = new("https://task-board.test/api/");

	private readonly List<TaskBoardCard> _cards =
	[
		new("card-1", "Write the release notes", "list-inbox", "normal", false, null),
		new("card-2", "Renew the certificate", "list-ops", "high", false, null),
		new("card-3", "Archive last season", "list-inbox", "low", true, null)
	];

	/// <summary>Set to make every request fail the way an unreachable server does.</summary>
	internal bool IsOffline { get; set; }

	internal IReadOnlyList<TaskBoardCard> Cards => _cards;

	internal IReadOnlyList<HttpRequestMessage> Requests { get; } = new List<HttpRequestMessage>();

	protected override async Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
	{
		((List<HttpRequestMessage>)Requests).Add(request);

		if (IsOffline)
		{
			throw new HttpRequestException("Connection refused.");
		}

		if (request.Headers.Authorization is not { Scheme: "Bearer", Parameter: ValidToken })
		{
			return new HttpResponseMessage(HttpStatusCode.Unauthorized);
		}

		var path = request.RequestUri!.AbsolutePath;

		if (request.Method == HttpMethod.Get && path.EndsWith("/lists", StringComparison.Ordinal))
		{
			return Json(new[] { new TaskBoardList("list-inbox", "Inbox"), new TaskBoardList("list-ops", "Operations") });
		}

		if (request.Method == HttpMethod.Get && path.EndsWith("/cards", StringComparison.Ordinal))
		{
			var openOnly = request.RequestUri.Query.Contains("open=true", StringComparison.Ordinal);
			return Json(_cards.Where(card => !openOnly || !card.Done).ToArray());
		}

		if (request.Method == HttpMethod.Post && path.EndsWith("/cards", StringComparison.Ordinal))
		{
			var body = (await request.Content!.ReadFromJsonAsync<CreateCardRequest>(cancellationToken))!;
			var created = new TaskBoardCard($"card-{_cards.Count + 1}", body.Title, body.ListId, body.Priority, false, body.DueAt);
			_cards.Add(created);
			return Json(created);
		}

		if (request.Method == HttpMethod.Post && path.EndsWith("/complete", StringComparison.Ordinal))
		{
			var id = path.Split('/')[^2];
			var index = _cards.FindIndex(card => card.Id == id);
			if (index < 0)
			{
				return new HttpResponseMessage(HttpStatusCode.NotFound);
			}

			_cards[index] = _cards[index] with { Done = true };
			return Json(_cards[index]);
		}

		return new HttpResponseMessage(HttpStatusCode.NotFound);
	}

	private static HttpResponseMessage Json<T>(T payload)
		=> new(HttpStatusCode.OK) { Content = JsonContent.Create(payload) };
}
```

## File: tests/MacroDeck.SampleRestApiPlugin.Tests/LocalizationTests.cs

```csharp
using NUnit.Framework;

namespace MacroDeck.SampleRestApiPlugin.Tests;

/// <summary>
/// The localization set is generated from <c>Localization/*.resx</c>, so these guard the wiring rather
/// than any wording: a missing catalog registration leaves every label showing its raw key, and a key
/// present in a translation but not in the default-language file can never resolve at all.
/// </summary>
[TestFixture]
public sealed class LocalizationTests
{
	[Test]
	public void The_catalog_is_scoped_to_the_plugin_id()
	{
		Assert.That(Strings.LocalizationCatalog.Scope, Is.EqualTo("plugin:app.macro-deck.sample-rest-api"));
	}

	[Test]
	public void English_is_the_default_culture()
	{
		Assert.That(Strings.LocalizationCatalog.DefaultCulture, Is.EqualTo("en"));
		Assert.That(Strings.LocalizationCatalog.Cultures, Does.Contain("en"));
	}

	[Test]
	public void The_action_strings_come_from_the_catalog()
	{
		Assert.That(Strings.LocalizationCatalog.KeysOf("en"), Does.Contain("Actions.RefreshBoard.Name"));
	}

	[Test]
	public void Every_key_the_default_culture_declares_resolves_to_text()
	{
		foreach (var key in Strings.LocalizationCatalog.KeysOf("en"))
		{
			Assert.That(Strings.LocalizationCatalog.TryGetTemplate("en", key, out var text), Is.True);
			Assert.That(text, Is.Not.Empty);
		}
	}

	/// <summary>
	/// Every culture the plugin ships carries every key the default language declares. MDLOC001 catches
	/// the other direction at build time - a key only a translation has - but a translation that is
	/// simply behind is not a build error, and this is what makes it a visible one.
	/// </summary>
	[Test]
	public void Every_culture_carries_every_key_the_default_language_declares()
	{
		var catalog = Strings.LocalizationCatalog;
		var expected = catalog.KeysOf(catalog.DefaultCulture);

		foreach (var culture in catalog.Cultures)
		{
			Assert.That(catalog.KeysOf(culture), Is.EquivalentTo(expected), $"culture '{culture}'");
		}
	}
}
```

## File: tests/MacroDeck.SampleRestApiPlugin.Tests/MacroDeck.SampleRestApiPlugin.Tests.csproj

```xml
<Project Sdk="Microsoft.NET.Sdk">

    <PropertyGroup>
        <IsPackable>false</IsPackable>
        <IsTestProject>true</IsTestProject>
        <!-- Underscored test names, like the Macro Deck repository's own test projects. -->
        <NoWarn>$(NoWarn);CA1707</NoWarn>
    </PropertyGroup>

    <ItemGroup>
        <PackageReference Include="MacroDeck.Plugin.Testing" />
        <PackageReference Include="Microsoft.NET.Test.Sdk" />
        <PackageReference Include="NUnit" />
        <PackageReference Include="NUnit.Analyzers" PrivateAssets="all" />
        <PackageReference Include="NUnit3TestAdapter" />
    </ItemGroup>

    <ItemGroup>
        <ProjectReference Include="..\..\src\MacroDeck.SampleRestApiPlugin\MacroDeck.SampleRestApiPlugin.csproj" />
    </ItemGroup>

</Project>
```

## File: tests/MacroDeck.SampleRestApiPlugin.Tests/TaskBoardConfigFlowTests.cs

```csharp
using MacroDeck.Plugin.Protocol.Capabilities.ConfigFlow;
using MacroDeck.Plugin.Testing;
using MacroDeck.SampleRestApiPlugin.Api;
using Microsoft.Extensions.DependencyInjection;
using NUnit.Framework;

namespace MacroDeck.SampleRestApiPlugin.Tests;

/// <summary>
/// The config flow driven step by step, the way the host drives it. Session state lives in the plugin
/// and is keyed by the session id the host mints, so every call here carries the same one.
/// </summary>
[TestFixture]
public sealed class TaskBoardConfigFlowTests
{
	private const string SessionId = "session-1";

	private static readonly Dictionary<string, object?> _noInput = [];

	[Test]
	public async Task The_flow_starts_by_asking_where_the_server_is()
	{
		await using var harness = await CreateAsync(new FakeTaskBoardApi());

		var result = (await harness.ConfigFlow.StartAsync(Start())).DataAs<ConfigFlowResultDto>();

		Assert.That(result!.Kind, Is.EqualTo("Step"));
		Assert.That(result.NextStep!.StepId, Is.EqualTo("server"));
		Assert.That(result.NextStep.Fields.Select(field => field.Name), Does.Contain("serverUrl"));
	}

	[Test]
	public async Task A_url_that_is_not_a_url_is_rejected_with_a_field_error()
	{
		await using var harness = await CreateAsync(new FakeTaskBoardApi());
		await harness.ConfigFlow.StartAsync(Start());

		var result = (await harness.ConfigFlow.SubmitAsync(Submit("server", new Dictionary<string, object?>
		{
			["serverUrl"] = "not a url",
			["authMethod"] = "token"
		}))).DataAs<ConfigFlowResultDto>();

		Assert.That(result!.Kind, Is.EqualTo("Error"));
		Assert.That(result.FieldErrors, Does.ContainKey("serverUrl"));
	}

	[Test]
	public async Task A_valid_server_leads_to_the_token_step()
	{
		await using var harness = await CreateAsync(new FakeTaskBoardApi());
		await harness.ConfigFlow.StartAsync(Start());

		var result = (await harness.ConfigFlow.SubmitAsync(Submit("server", ServerInput()))).DataAs<ConfigFlowResultDto>();

		Assert.That(result!.Kind, Is.EqualTo("Step"));
		Assert.That(result.NextStep!.StepId, Is.EqualTo("token"));
		Assert.That(result.NextStep.Fields.Single().Type, Is.EqualTo("Secret"));
	}

	[Test]
	public async Task A_token_the_server_rejects_never_completes_the_entry()
	{
		await using var harness = await CreateAsync(new FakeTaskBoardApi());
		await harness.ConfigFlow.StartAsync(Start());
		await harness.ConfigFlow.SubmitAsync(Submit("server", ServerInput()));

		var result = (await harness.ConfigFlow.SubmitAsync(Submit("token",
			new Dictionary<string, object?> { ["token"] = "nonsense" }))).DataAs<ConfigFlowResultDto>();

		Assert.That(result!.Kind, Is.EqualTo("Error"));
		// Flattened into the plugin's own language here, because this harness has no connection and so no
		// negotiated protocol version - see TaskBoardIntegrationTests for the full reason.
		Assert.That(result.ErrorMessage?.Literal, Does.Contain("rejected the token"));
	}

	[Test]
	public async Task A_verified_token_completes_and_is_stored_as_a_secret()
	{
		await using var harness = await CreateAsync(new FakeTaskBoardApi());
		await harness.ConfigFlow.StartAsync(Start());
		await harness.ConfigFlow.SubmitAsync(Submit("server", ServerInput()));

		var result = (await harness.ConfigFlow.SubmitAsync(Submit("token",
			new Dictionary<string, object?> { ["token"] = FakeTaskBoardApi.ValidToken }))).DataAs<ConfigFlowResultDto>();

		Assert.That(result!.Kind, Is.EqualTo("Complete"));
		Assert.That(result.EntryTitle, Does.Contain("task-board.test"));
		Assert.That(result.Values!["serverUrl"].IsSecret, Is.False);
		Assert.That(result.Values["token"].IsSecret, Is.True);
		Assert.That(result.Values["token"].Value, Is.EqualTo(FakeTaskBoardApi.ValidToken));
	}

	[Test]
	public async Task Choosing_to_sign_in_sends_the_user_to_the_authorization_page()
	{
		await using var harness = await CreateAsync(new FakeTaskBoardApi());
		await harness.ConfigFlow.StartAsync(Start());

		var input = ServerInput();
		input["authMethod"] = "oauth";
		var result = (await harness.ConfigFlow.SubmitAsync(Submit("server", input))).DataAs<ConfigFlowResultDto>();

		Assert.That(result!.Kind, Is.EqualTo("External"));
		Assert.That(result.ResumeStepId, Is.EqualTo("oauth-callback"));
		Assert.That(result.ExternalUrl, Does.Contain("redirect_uri=http%3A%2F%2Flocalhost%2Fcallback"));
		Assert.That(result.ExternalUrl, Does.Contain("state=state-1"));
	}

	[Test]
	public async Task Coming_back_without_a_code_starts_over_instead_of_completing()
	{
		await using var harness = await CreateAsync(new FakeTaskBoardApi());
		await harness.ConfigFlow.StartAsync(Start());

		var input = ServerInput();
		input["authMethod"] = "oauth";
		await harness.ConfigFlow.SubmitAsync(Submit("server", input));

		var result = (await harness.ConfigFlow.SubmitAsync(Submit("oauth-callback", _noInput)))
			.DataAs<ConfigFlowResultDto>();

		Assert.That(result!.Kind, Is.EqualTo("Error"));
		Assert.That(result.NextStep!.StepId, Is.EqualTo("server"));
	}

	[Test]
	public async Task Coming_back_with_a_code_completes_the_entry()
	{
		await using var harness = await CreateAsync(new FakeTaskBoardApi());
		await harness.ConfigFlow.StartAsync(Start());

		var input = ServerInput();
		input["authMethod"] = "oauth";
		await harness.ConfigFlow.SubmitAsync(Submit("server", input));

		var result = (await harness.ConfigFlow.SubmitAsync(
			Submit("oauth-callback", _noInput, authorizationCode: FakeTaskBoardApi.ValidToken))).DataAs<ConfigFlowResultDto>();

		Assert.That(result!.Kind, Is.EqualTo("Complete"));
		Assert.That(result.Values!["token"].IsSecret, Is.True);
	}

	[Test]
	public async Task An_unknown_step_is_refused_rather_than_treated_as_the_current_one()
	{
		await using var harness = await CreateAsync(new FakeTaskBoardApi());
		await harness.ConfigFlow.StartAsync(Start());

		var result = (await harness.ConfigFlow.SubmitAsync(Submit("who-knows", _noInput))).DataAs<ConfigFlowResultDto>();

		Assert.That(result!.Kind, Is.EqualTo("Error"));
	}

	private static Dictionary<string, object?> ServerInput() => new()
	{
		["serverUrl"] = FakeTaskBoardApi.BaseAddress.ToString(),
		["authMethod"] = "token"
	};

	private static FlowStartArguments Start() => new() { SessionId = SessionId, OAuth = OAuth() };

	private static FlowSubmitArguments Submit(
		string stepId,
		IReadOnlyDictionary<string, object?> input,
		string? authorizationCode = null)
		=> new()
		{
			SessionId = SessionId,
			StepId = stepId,
			Input = input.ToDictionary(pair => pair.Key,
				pair => System.Text.Json.JsonSerializer.SerializeToElement(pair.Value),
				StringComparer.Ordinal),
			OAuth = OAuth(authorizationCode)
		};

	private static ConfigFlowOAuthContextDto OAuth(string? authorizationCode = null) => new()
	{
		RedirectUri = "http://localhost/callback",
		State = "state-1",
		AuthorizationCode = authorizationCode
	};

	private static async Task<PluginTestHarness> CreateAsync(FakeTaskBoardApi api)
	{
		var harness = PluginTestHarness.Create(builder =>
		{
			builder.UseLocalization(Strings.LocalizationCatalog).RegisterIntegration<RestApiIntegration>();
			builder.Services.AddTaskBoardApi().ConfigurePrimaryHttpMessageHandler(() => api);
		});

		await harness.InitializeIntegrationsAsync();
		return harness;
	}
}
```

## File: tests/MacroDeck.SampleRestApiPlugin.Tests/TaskBoardIntegrationTests.cs

```csharp
using MacroDeck.Plugin.Protocol.Capabilities.Actions;
using MacroDeck.Plugin.Protocol.Capabilities.Issues;
using MacroDeck.Plugin.Protocol.Capabilities.Variables;
using MacroDeck.Plugin.Testing;
using MacroDeck.SampleRestApiPlugin.Api;
using Microsoft.Extensions.DependencyInjection;
using NUnit.Framework;

namespace MacroDeck.SampleRestApiPlugin.Tests;

[TestFixture]
public sealed class TaskBoardIntegrationTests
{
	[Test]
	public async Task An_unconfigured_integration_reports_an_issue_instead_of_failing_quietly()
	{
		await using var harness = await CreateAsync(new FakeTaskBoardApi(), configured: false);

		var issues = (await harness.Issues.GetIssuesAsync()).DataAs<IssueListResult>();
		var configured = (await harness.Variables.GetAsync("configured")).DataAs<VariableReadingDto>();
		var openCards = (await harness.Variables.GetAsync("open-cards")).DataAs<VariableReadingDto>();

		Assert.That(issues!.Issues.Single().Id, Is.EqualTo("not-configured"));
		Assert.That(issues.Issues[0].Severity, Is.EqualTo("Error"));
		Assert.That(configured!.Value.Boolean, Is.False);
		Assert.That(openCards!.Value.Kind, Is.EqualTo("unavailable"), "an unconfigured count is unknown, not zero");
	}

	[Test]
	public async Task An_action_run_before_configuration_says_so()
	{
		await using var harness = await CreateAsync(new FakeTaskBoardApi(), configured: false);

		var outcome = await harness.Actions.ExecuteAsync("refresh-board");

		Assert.That(outcome.Succeeded, Is.False);
		// Text this plugin produces is a reference, not a sentence, so what a reader ends up seeing is
		// decided by whoever resolves it. In this harness nothing does: there is no connection to
		// negotiate a protocol version on, so the SDK flattens every reference against the plugin's own
		// catalog in its own default language - which is only possible because the harness registers that
		// catalog. Drop the UseLocalization call above and this assertion sees a blank message.
		Assert.That(outcome.Error!.Message, Does.Contain("not configured"));
	}

	[Test]
	public async Task A_configured_integration_reads_the_board_and_has_no_issues()
	{
		await using var harness = await CreateAsync(new FakeTaskBoardApi());

		var issues = (await harness.Issues.GetIssuesAsync()).DataAs<IssueListResult>();
		var openCards = (await harness.Variables.GetAsync("open-cards")).DataAs<VariableReadingDto>();
		var next = (await harness.Variables.GetAsync("next-card")).DataAs<VariableReadingDto>();

		Assert.That(issues!.Issues, Is.Empty);
		Assert.That(openCards!.Value.Number, Is.EqualTo(2), "the third card is already done");
		Assert.That(next!.Value.Text, Is.EqualTo("Write the release notes"));
	}

	[Test]
	public async Task A_rejected_token_becomes_an_issue_that_hands_the_user_back_to_the_config_flow()
	{
		await using var harness = await CreateAsync(new FakeTaskBoardApi(), token: "expired-token");

		var issues = (await harness.Issues.GetIssuesAsync()).DataAs<IssueListResult>();
		Assert.That(issues!.Issues.Single().Id, Is.EqualTo("unauthorized"));

		var resolution = (await harness.Issues.ResolveAsync(new IssueResolveArguments { IssueId = "unauthorized" }))
			.DataAs<IssueResolveResult>();

		Assert.That(resolution!.Success, Is.True);
		Assert.That(resolution.FollowUp, Is.EqualTo("StartConfigFlow"));
	}

	[Test]
	public async Task An_unreachable_server_is_a_warning_and_retrying_it_reports_the_truth()
	{
		var api = new FakeTaskBoardApi { IsOffline = true };
		await using var harness = await CreateAsync(api);

		var issues = (await harness.Issues.GetIssuesAsync()).DataAs<IssueListResult>();
		Assert.That(issues!.Issues.Single().Id, Is.EqualTo("unreachable"));
		Assert.That(issues.Issues[0].Severity, Is.EqualTo("Warning"));

		// Retrying while the server is still down reports the real reason rather than pretending to fix it.
		var retried = (await harness.Issues.ResolveAsync(new IssueResolveArguments { IssueId = "unreachable" }))
			.DataAs<IssueResolveResult>();
		Assert.That(retried!.Success, Is.False);
		Assert.That(retried.Message?.Literal, Does.Contain("unreachable"));

		// Once the server answers again the issue is simply gone: the list is live, never cached.
		api.IsOffline = false;
		var afterRecovery = (await harness.Issues.GetIssuesAsync()).DataAs<IssueListResult>();
		Assert.That(afterRecovery!.Issues, Is.Empty);
	}

	[Test]
	public async Task A_failing_read_notifies_the_user_once_and_dismisses_it_on_recovery()
	{
		var api = new FakeTaskBoardApi { IsOffline = true };
		await using var harness = await CreateAsync(api);

		await harness.Actions.ExecuteAsync("refresh-board");
		Assert.That(harness.Context.Notifications.Current, Is.Not.Empty);

		api.IsOffline = false;
		await harness.Actions.ExecuteAsync("refresh-board");
		Assert.That(harness.Context.Notifications.Current, Is.Empty);
	}

	[Test]
	public async Task Creating_a_card_sends_what_was_configured_and_shows_up_in_the_board()
	{
		var api = new FakeTaskBoardApi();
		await using var harness = await CreateAsync(api);

		var outcome = await harness.Actions.ExecuteAsync("create-card", new Dictionary<string, object?>
		{
			["title"] = "Order more coffee",
			["listId"] = "list-ops",
			["priority"] = "high",
			["notes"] = "The good one."
		});

		var created = api.Cards[^1];
		var openCards = (await harness.Variables.GetAsync("open-cards")).DataAs<VariableReadingDto>();

		Assert.That(outcome.Succeeded, Is.True);
		Assert.That(created.Title, Is.EqualTo("Order more coffee"));
		Assert.That(created.ListId, Is.EqualTo("list-ops"));
		Assert.That(created.Priority, Is.EqualTo("high"));
		Assert.That(openCards!.Value.Number, Is.EqualTo(3));
	}

	[Test]
	public async Task Creating_a_card_without_a_title_never_reaches_the_api()
	{
		var api = new FakeTaskBoardApi();
		await using var harness = await CreateAsync(api);
		var requestsBefore = api.Requests.Count;

		var outcome = await harness.Actions.ExecuteAsync("create-card",
			new Dictionary<string, object?> { ["listId"] = "list-ops" });

		Assert.That(outcome.Succeeded, Is.False);
		Assert.That(api.Requests, Has.Count.EqualTo(requestsBefore));
	}

	[Test]
	public async Task Completing_a_card_publishes_it_and_takes_it_off_the_open_list()
	{
		var api = new FakeTaskBoardApi();
		await using var harness = await CreateAsync(api);

		var outcome = await harness.Actions.ExecuteAsync("complete-card",
			new Dictionary<string, object?> { ["cardId"] = "card-1" });

		var published = harness.Context.Events.Published[^1];
		var openCards = (await harness.Variables.GetAsync("open-cards")).DataAs<VariableReadingDto>();

		Assert.That(outcome.Succeeded, Is.True);
		Assert.That(published.EventId, Is.EqualTo("card-completed"));
		Assert.That(published.Parameters!.Value.GetProperty("title").GetString(), Is.EqualTo("Write the release notes"));
		Assert.That(openCards!.Value.Number, Is.EqualTo(1));
	}

	[Test]
	public async Task A_card_the_server_does_not_know_fails_as_not_found()
	{
		await using var harness = await CreateAsync(new FakeTaskBoardApi());

		var outcome = await harness.Actions.ExecuteAsync("complete-card",
			new Dictionary<string, object?> { ["cardId"] = "card-404" });

		Assert.That(outcome.Succeeded, Is.False);
		Assert.That(outcome.Error!.Message, Does.Contain("does not know"));
	}

	[Test]
	public async Task A_rejected_token_fails_the_action_differently_from_an_unreachable_server()
	{
		var api = new FakeTaskBoardApi();
		await using var harness = await CreateAsync(api, token: "expired-token");
		var unauthorized = await harness.Actions.ExecuteAsync("refresh-board");

		await using var offline = await CreateAsync(new FakeTaskBoardApi { IsOffline = true });
		var unreachable = await offline.Actions.ExecuteAsync("refresh-board");

		Assert.That(unauthorized.Error!.Message, Does.Contain("rejected the token"));
		Assert.That(unreachable.Error!.Message, Does.Contain("unreachable"));
	}

	[Test]
	public async Task List_options_come_from_the_api()
	{
		await using var harness = await CreateAsync(new FakeTaskBoardApi());

		var options = (await harness.Actions.GetOptionsAsync("create-card", "listId")).DataAs<DynamicOptionsResultDto>();

		// A list's name comes from the API, so it stays a literal all the way onto the wire.
		Assert.That(options!.Options.Select(option => option.Label?.Literal), Is.EquivalentTo(_listNames));
	}

	[Test]
	public async Task Card_options_are_filtered_by_what_the_user_typed()
	{
		await using var harness = await CreateAsync(new FakeTaskBoardApi());

		var options = (await harness.Actions.GetOptionsAsync("complete-card", "cardId", filter: "certificate"))
			.DataAs<DynamicOptionsResultDto>();

		Assert.That(options!.Options.Single().Value, Is.EqualTo("card-2"));
	}

	[Test]
	public async Task Options_are_empty_rather_than_broken_while_the_server_is_unreachable()
	{
		await using var harness = await CreateAsync(new FakeTaskBoardApi { IsOffline = true });

		var outcome = await harness.Actions.GetOptionsAsync("create-card", "listId");

		Assert.That(outcome.Succeeded, Is.True);
		Assert.That(outcome.DataAs<DynamicOptionsResultDto>()!.Options, Is.Empty);
	}

	private static readonly string[] _listNames = ["Inbox", "Operations"];

	private static async Task<PluginTestHarness> CreateAsync(
		FakeTaskBoardApi api,
		bool configured = true,
		string token = FakeTaskBoardApi.ValidToken)
	{
		var harness = PluginTestHarness.Create(builder =>
		{
			builder.UseLocalization(Strings.LocalizationCatalog).RegisterIntegration<RestApiIntegration>();
			builder.Services.AddTaskBoardApi().ConfigurePrimaryHttpMessageHandler(() => api);
		});

		if (configured)
		{
			// What the config flow would have persisted, seeded directly so these tests are about the
			// integration rather than about the wizard.
			var entryId = harness.Context.Config.AddEntry("Task Board");
			harness.Context.Config.SeedString(entryId, "serverUrl", FakeTaskBoardApi.BaseAddress.ToString());
			harness.Context.Config.SeedSecret(entryId, "token", token);
		}

		await harness.InitializeIntegrationsAsync();
		return harness;
	}
}
```
