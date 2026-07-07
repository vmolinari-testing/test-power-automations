import express from "express";
import {
    ActivityHandler,
    CardFactory,
    CloudAdapter,
    ConfigurationServiceClientCredentialFactory,
    createBotFrameworkAuthenticationFromConfiguration,
    TurnContext,
} from "botbuilder";

import { settings } from "./config.js";
import { mockData } from "./data.js";

const app = express();

app.use(express.json());

const credentialsFactory = new ConfigurationServiceClientCredentialFactory({
    MicrosoftAppId: settings.microsoftAppId,
    MicrosoftAppPassword: settings.microsoftAppPassword,
    MicrosoftAppType: settings.microsoftAppType,
    MicrosoftAppTenantId: settings.microsoftAppTenantId,
});

const botFrameworkAuthentication =
    createBotFrameworkAuthenticationFromConfiguration(null, credentialsFactory);

const adapter = new CloudAdapter(botFrameworkAuthentication);

adapter.onTurnError = async (
    context: TurnContext,
    error: Error,
): Promise<void> => {
    console.error("Bot error:", error);
    await context.sendActivity(
        "Si è verificato un errore durante la gestione del messaggio.",
    );
};

class TeamsBot extends ActivityHandler {
    public constructor() {
        super();

        this.onMessage(async (context, next) => {
            const action = context.activity.value?.action;

            if (action === "create_ticket") {
                await context.sendActivity(
                    "Richiesta ticket ricevuta correttamente.",
                );
                await next();
                return;
            }

            await context.sendActivity({
                attachments: [CardFactory.adaptiveCard(buildTicketCard())],
            });

            await next();
        });
    }
}

const bot = new TeamsBot();

app.get("/", (_request, response) => {
    response.json({ status: "ok" });
});

app.get("/automations", (_request, response) => {
    response.json(mockData);
});

app.get("/privacy", (_request, response) => {
    response.json({
        title: "Privacy Policy",
        content:
            "This is a private test application used to validate a Microsoft Teams integration with a middleware. No production data is stored by this test service.",
    });
});

app.get("/tos", (_request, response) => {
    response.json({
        title: "Terms of Service",
        content:
            "This service is provided only for internal testing of a Microsoft Teams bot and Adaptive Card workflow. It is not intended for production use.",
    });
});

app.post("/api/messages", async (request, response) => {
    await adapter.process(request, response, async (context) => {
        await bot.run(context);
    });
});

function buildTicketCard(): Record<string, unknown> {
    return {
        $schema: "http://adaptivecards.io/schemas/adaptive-card.json",
        type: "AdaptiveCard",
        version: "1.4",
        body: [
            {
                type: "TextBlock",
                text: "Apertura ticket automazione RPA",
                weight: "Bolder",
                size: "Medium",
            },
            {
                type: "Input.ChoiceSet",
                id: "automation",
                label: "Automazione",
                style: "compact",
                isMultiSelect: false,
                choices: mockData,
            },
            {
                type: "Input.Text",
                id: "description",
                label: "Descrizione problema",
                isMultiline: true,
                placeholder: "Descrivi brevemente il problema...",
            },
        ],
        actions: [
            {
                type: "Action.Submit",
                title: "Apri ticket",
                data: {
                    action: "create_ticket",
                },
            },
        ],
    };
}

app.listen(settings.port, () => {
    console.log(`Server listening on port ${settings.port}`);
    console.log(
        `MICROSOFT_APP_ID prefix: ${settings.microsoftAppId.slice(0, 8)}`,
    );
    console.log(`MICROSOFT_APP_ID length: ${settings.microsoftAppId.length}`);
    console.log(
        `MICROSOFT_APP_PASSWORD configured: ${Boolean(
            settings.microsoftAppPassword,
        )}`,
    );
    console.log(
        `MICROSOFT_APP_PASSWORD length: ${settings.microsoftAppPassword.length}`,
    );
    console.log(`MICROSOFT_APP_TYPE: ${settings.microsoftAppType}`);
    console.log(
        `MICROSOFT_APP_TENANT_ID length: ${settings.microsoftAppTenantId.length}`,
    );
});
