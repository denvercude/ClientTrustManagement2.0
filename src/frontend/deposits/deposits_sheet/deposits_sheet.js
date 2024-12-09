document.addEventListener("DOMContentLoaded", () => {
    loadHeader("Daily Deposits Sheet");

    const tableBody = document.querySelector("#deposits-sheet-table tbody");

    const fields = ["First Name", "Last Name", "Type", "Amount"];

    for (let i = 0; i < 5; i++) {
        addRow(tableBody, fields);
    }

    document.getElementById("add-row").addEventListener("click", () => {
        addRow(tableBody, fields);
    });

    document.getElementById("add-all").addEventListener("click", async () => {
        const rows = Array.from(tableBody.querySelectorAll("tr"));
        const validTypes = ["Credit", "Visa", "Master", "Amex", "Cash", "Check"];
        const deposits = [];
        const successList = document.querySelector("#success-list");
        const errorList = document.querySelector("#error-list");

        clearStatusLists()

        for (const row of rows) {
            const inputs = row.querySelectorAll("input");
            let amount = parseFloat(inputs[3].value.trim());
            if (isNaN(amount)) {
                amount = 0;
            }

            first_name = inputs[0].value.trim();
            last_name = inputs[1].value.trim();
            const type = inputs[2].value.trim();

            if (!validTypes.includes(type)) {
                const li = document.createElement("li");
                li.textContent = `${last_name} - Invalid Deposit Type - ${type}`;
                li.classList.add("error");
                errorList.appendChild(li);
                return;
            }

            deposits.push({
                first_name: inputs[0].value.trim(),
                last_name: inputs[1].value.trim(),
                type: type,
                amount: amount
            });

            const li = document.createElement("li");
            li.textContent = `${last_name} - ${type} - ${amount}`;
            li.classList.add("success");
            successList.appendChild(li);
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/create-deposits/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({deposits})
            });

            const result = await response.json();
            if (response.ok) {
                alert(result.message);
            } else {
                const errorMessage = result.detail.message || "An unknown error occurred";
                alert(`Error: ${errorMessage}`);
            }
        } catch (error) {
            console.error('Fetch Error:', error);
            alert("An error occurred while communicating with the server: " + (error.message || "No detailed error message available"));
        }
    });

    document.getElementById("clear-list").addEventListener("click", async () => {
        clearStatusLists()
      });

});