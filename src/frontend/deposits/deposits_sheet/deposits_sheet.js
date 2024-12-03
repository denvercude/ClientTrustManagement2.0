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
        const deposits = rows.map(row => {
            const inputs = row.querySelectorAll("input");
            return {
                first_name: inputs[0].value.trim(),
                last_name: inputs[1].value.trim(),
                type: inputs[2].value.trim(),
                amount: inputs[3].value.trim()
            };
        });
    
        try {
            const response = await fetch('http://127.0.0.1:8000/create-deposits/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ deposits })
            });
    
            const result = await response.json();
            if (response.ok) {
                console.log(result.message);
                alert("Deposit sheet created successfully");
            } else {
                console.error('Error Response:', result);
                alert("Failed to create deposit sheet: " + (result.detail || "Unknown error"));
            }
        } catch (error) {
            console.error('Fetch Error:', error);
            alert("An error occurred while creating the deposit sheet.");
        }
    });

});