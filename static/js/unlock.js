document.addEventListener("DOMContentLoaded", () => {

    let currentAd = 1;
    let checking = false;

    const progressBar = document.getElementById("progressBar");
    const step = document.getElementById("step");
    const total = document.getElementById("total");
    const finalButton = document.getElementById("finalButton");

    total.innerText = TOTAL_ADS;
    finalButton.disabled = true;

    function updateProgress() {

        progressBar.style.width = ((currentAd - 1) / TOTAL_ADS) * 100 + "%";

        step.innerText = currentAd <= TOTAL_ADS ? currentAd : TOTAL_ADS;

    }

    async function checkAd() {

        if (checking) return;

        checking = true;

        const btn = document.getElementById("btn" + currentAd);

        const res = await fetch("/api/check-ad", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                code: LINK_CODE

            })

        });

        const data = await res.json();

        checking = false;

        if (!data.success) {

            if (data.remaining !== undefined) {

                btn.innerHTML =
                    "⏳ Watch Ad 15 Seconds Minimum (" +
                    data.remaining +
                    "s)";

                btn.disabled = true;

                setTimeout(checkAd, 1000);

            }

            return;

        }

        btn.innerHTML = "✅ Completed";

        btn.disabled = true;

        btn.classList.remove("active-btn");

        btn.classList.add("complete-btn");

        currentAd++;

        updateProgress();

        if (currentAd <= TOTAL_ADS) {

            const next = document.getElementById("btn" + currentAd);

            next.disabled = false;

            next.classList.remove("lock-btn");

            next.classList.add("active-btn");

            next.innerHTML = "▶ WATCH NOW";

        }

        else {

            finalButton.disabled = false;

        }

    }

    for (let i = 1; i <= TOTAL_ADS; i++) {

        const btn = document.getElementById("btn" + i);

        if (!btn) continue;

        if (i !== 1)
            btn.disabled = true;

        btn.onclick = async function () {

            if (i !== currentAd)
                return;

            const res = await fetch("/api/start-ad", {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    code: LINK_CODE,

                    ad: i

                })

            });

            const data = await res.json();

            if (!data.success) {

                alert(data.message);

                return;

            }

            btn.disabled = true;

            btn.innerHTML = "⏳ Watch Ad 15 Seconds Minimum";

            window.location.href = data.smartlink;

        };

    }

    window.addEventListener("focus", function () {

        checkAd();

    });

    finalButton.onclick = async function () {

        const res = await fetch("/api/unlock", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                code: LINK_CODE

            })

        });

        const data = await res.json();

        if (!data.success) {

            alert(data.message);

            return;

        }

        window.location.href = data.url;

    };

    updateProgress();

});
