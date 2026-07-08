type AutomationChoice = {
    title: string;
    value: string;
};

type TicketResponse = {
    status: string;
    ticket_id: string;
    automation: string;
};

const automationSelect = document.getElementById(
    "automation",
) as HTMLSelectElement | null;

const form = document.getElementById("ticket-form") as HTMLFormElement | null;
const result = document.getElementById("result") as HTMLDivElement | null;

if (!automationSelect || !form || !result) {
    throw new Error("Required DOM elements not found");
}

function createOption(value: string, text: string): HTMLOptionElement {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = text;
    return option;
}

async function loadAutomations(): Promise<void> {
    try {
        const response = await fetch("/api/v1/automations");

        if (!response.ok) {
            throw new Error("Automation request failed");
        }

        const automations = (await response.json()) as AutomationChoice[];

        automationSelect!.replaceChildren(
            createOption("", "Seleziona automazione"),
        );

        for (const automation of automations) {
            automationSelect!.appendChild(
                createOption(automation.value, automation.title),
            );
        }
    } catch {
        automationSelect!.replaceChildren(
            createOption("", "Errore caricamento automazioni"),
        );
    }
}

function showSuccess(message: string): void {
    result!.className = "result success";
    result!.textContent = message;
}

function showError(message: string): void {
    result!.className = "result error";
    result!.textContent = message;
}

function clearResult(): void {
    result!.className = "result";
    result!.textContent = "";
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    clearResult();

    const formData = new FormData(form);

    const payload = {
        automation: String(formData.get("automation") ?? ""),
        description: String(formData.get("description") ?? ""),
    };

    try {
        const response = await fetch("/api/v1/tickets", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            throw new Error("Ticket creation failed");
        }

        const data = (await response.json()) as TicketResponse;

        showSuccess(
            `Segnalazione inviata correttamente. Ticket: ${data.ticket_id}`,
        );

        form.reset();
        await loadAutomations();
    } catch {
        showError("Non è stato possibile inviare la segnalazione.");
    }
});

void loadAutomations();
