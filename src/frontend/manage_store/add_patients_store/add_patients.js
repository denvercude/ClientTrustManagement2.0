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

    const accountList = document.createElement("ul");

    accounts.forEach(account => {
        const listItem = document.createElement("li");
        listItem.textContent = `${account.lastName}, ${account.firstName} - $${account.storeCredit}`;
        accountList.appendChild(listItem);
    });

    container.appendChild(accountList);
}

function displayNewAccounts(accounts) {
    const container = document.getElementById("new-accounts-list");

    container.innerHTML = "";

    const accountList = document.createElement("ul");

    accounts.forEach(account => {
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