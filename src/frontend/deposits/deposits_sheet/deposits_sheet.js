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
            let amount = parseFloat(inputs[3].value.trim());
            if (isNaN(amount)) {
                amount = 0;
            }
            return {
                first_name: inputs[0].value.trim(),
                last_name: inputs[1].value.trim(),
                type: inputs[2].value.trim(),
                amount: amount
            };
        });

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
                const errorMessage = result.message || result.detail || "An unknown error occurred";
                throw new Error(`Server responded with status: ${response.status}, Error: ${errorMessage}`);
            }
        } catch (error) {
            console.error('Fetch Error:', error);
            alert("An error occurred while communicating with the server: " + (error.message || "No detailed error message available"));
        }
    });

});