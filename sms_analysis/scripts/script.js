document.addEventListener("DOMContentLoaded", function () {
    const filterDropdown = document.getElementById("filter");
    const transactionsDiv = document.getElementById("transactions");
    const ctx = document.getElementById("transactionChart").getContext("2d");
    let chart;

    async function fetchTransactions(filter = "") {
        let url = "http://127.0.0.1:5000/transactions";
        if (filter) {
            url += `?type=${encodeURIComponent(filter)}`;
        }
        
        const response = await fetch(url);
        const transactions = await response.json();
        displayTransactions(transactions);
        updateChart(transactions);
    }

    function displayTransactions(transactions) {
        transactionsDiv.innerHTML = "";
        transactions.forEach(tx => {
            const txElement = document.createElement("div");
            txElement.textContent = `${tx.date} - ${tx.type}: ${tx.amount} RWF`;
            transactionsDiv.appendChild(txElement);
        });
    }

    function updateChart(transactions) {
        const counts = {};
        transactions.forEach(tx => {
            counts[tx.type] = (counts[tx.type] || 0) + 1;
        });
        
        const labels = Object.keys(counts);
        const data = Object.values(counts);

        if (chart) {
            chart.destroy();
        }

        chart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: "Transaction Count",
                    data: data,
                    backgroundColor: "#007bff",
                }]
            }
        });
    }

    filterDropdown.addEventListener("change", function () {
        fetchTransactions(filterDropdown.value);
    });

    fetchTransactions();
});
