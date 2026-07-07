import dotenv from "dotenv";

dotenv.config();

type Settings = {
    microsoftAppId: string;
    microsoftAppPassword: string;
    microsoftAppType: string;
    microsoftAppTenantId: string;
    port: number;
};

function getRequiredEnv(name: string): string {
    const value = process.env[name];

    if (!value) {
        throw new Error(`Missing required environment variable: ${name}`);
    }

    return value;
}

export const settings: Settings = {
    microsoftAppId: getRequiredEnv("MICROSOFT_APP_ID"),
    microsoftAppPassword: getRequiredEnv("MICROSOFT_APP_PASSWORD"),
    microsoftAppType: process.env.MICROSOFT_APP_TYPE ?? "SingleTenant",
    microsoftAppTenantId: getRequiredEnv("MICROSOFT_APP_TENANT_ID"),
    port: Number(process.env.PORT ?? 3978),
};
