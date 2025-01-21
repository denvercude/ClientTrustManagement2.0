document.addEventListener("DOMContentLoaded", async () => {
    loadHeader("Add Accounts to Store");

    const current_accounts = await fetchCurrentAccounts();
    displayCurrentAccounts(current_accounts);

    const new_accounts = await fetchNewAccounts();
    displayNewAccounts(new_accounts)
});

function displayCurrentAccounts(accounts) {
    const container = document.getElementById("current-accounts-list");

    container.innerHTML = "";

    const sortedAccounts = accounts.sort((a, b) => a.lastName.localeCompare(b.lastName));

    const accountList = document.createElement("ul");

    sortedAccounts.forEach(account => {
        const listItem = document.createElement("li");
        listItem.textContent = `${account.lastName}, ${account.firstName} - $${account.storeCredit}`;
        accountList.appendChild(listItem);
    });

    container.appendChild(accountList);
}

function displayNewAccounts(accounts) {
    const container = document.getElementById("new-accounts-list");

    container.innerHTML = "";

    const sortedAccounts = accounts.sort((a, b) => a.lastName.localeCompare(b.lastName));

    const accountList = document.createElement("ul");

    sortedAccounts.forEach(account => {
        const listItem = document.createElement("li");
        listItem.textContent = `${account.lastName}, ${account.firstName}`;
        accountList.appendChild(listItem);
    });

    container.appendChild(accountList);
}

async function fetchCurrentAccounts() {
    try {
        const response = await fetch("http://127.0.0.1:8000/current-accounts/");
        if (response.ok) {
            const data = await response.json();
            return data.accounts;
        } else {
            console.error("Failed to fetch current accounts:", response.status);
            return [];
        }
    } catch (error) {
        console.error("Error fetching current accounts:", error);
        return [];
    }
}

async function fetchNewAccounts() {
    try{
        const response = await fetch("http://127.0.0.1:8000/new-accounts/");
        if (response.ok) {
            const data = await response.json();
            return data.accounts;
        } else {
            console.error("Failed to fetch current accounts:", response.status);
            return [];
        }
    } catch (error){
        console.error("Error fetching new accounts:", error);
        return [];
    }
}

document.getElementById("add-accounts").addEventListener("click", async () => {
    try {
        const response = await fetch("http://127.0.0.1:8000/add-accounts/");
        if (response.ok) {
            const data = await response.json();
            const successfullyAdded = data.accounts.successfullyAdded;
            const failedAccounts = data.accounts.failedAccounts;

            // Display the results
            displaySuccessfullyAddedAccounts(successfullyAdded);
            displayFailedAccounts(failedAccounts);
        } else {
            console.error("Error adding accounts:", response.statusText);
        }
    } catch (error) {
        console.error("Error occurred while adding accounts:", error);
    }
});

function displaySuccessfullyAddedAccounts(accounts) {
    const container = document.querySelector(".status-list h3:nth-of-type(1)").nextElementSibling;

    // Clear existing content if any
    container.innerHTML = "";

    // Create and append list of successfully added accounts
    const successList = document.createElement("ul");
    accounts.forEach(account => {
        const listItem = document.createElement("li");
        listItem.textContent = `${account.lastName}, ${account.firstName}`;
        successList.appendChild(listItem);
    });

    container.appendChild(successList);
}

function displayFailedAccounts(accounts) {
    const container = document.querySelector(".status-list h3:nth-of-type(2)").nextElementSibling;

    // Clear existing content if any
    container.innerHTML = "";

    // Create and append list of failed accounts
    const failedList = document.createElement("ul");
    accounts.forEach(account => {
        const listItem = document.createElement("li");
        listItem.textContent = `${account.lastName}, ${account.firstName} - Error: ${account.error || "Unknown error"}`;
        failedList.appendChild(listItem);
    });

    container.appendChild(failedList);
}