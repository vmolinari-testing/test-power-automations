import { app, pages } from "@microsoft/teams-js";

const tabUrl = "https://test-power-automations.onrender.com/tab/open-ticket";

async function initializeTeamsConfig(): Promise<void> {
    await app.initialize();

    pages.config.registerOnSaveHandler((saveEvent) => {
        pages.config.setConfig({
            entityId: "open-ticket",
            suggestedDisplayName: "Apri segnalazione",
            contentUrl: tabUrl,
            websiteUrl: tabUrl,
        });

        saveEvent.notifySuccess();
    });

    pages.config.setValidityState(true);
}

void initializeTeamsConfig();
