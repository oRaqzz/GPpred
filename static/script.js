document.getElementById("predictionForm").addEventListener("submit", async function(e) {
    e.preventDefault()

    const Open = parseFloat(document.getElementById("Open").value)
    const High = parseFloat(document.getElementById("High").value)
    const Low = parseFloat(document.getElementById("Low").value)
    const Close = parseFloat(document.getElementById("Close").value)
    const Volume = parseFloat(document.getElementById("Volume").value)
    const Date = document.getElementById("Date").value

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ Open, High, Low, Close, Volume, Date })
        })

        const data = await response.json();
        document.getElementById("result").innerText = `Prediction: ${data.prediction}`
    } catch (e) {
        console.error("Error:", e)
    }
})