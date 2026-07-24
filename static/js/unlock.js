document.addEventListener("DOMContentLoaded", () => {

    let currentAd = 1;

    const progressBar = document.getElementById("progressBar");
    const step = document.getElementById("step");
    const total = document.getElementById("total");
    const finalButton = document.getElementById("finalButton");

    total.innerText = TOTAL_ADS;

    function updateProgress() {

        const percent = ((currentAd - 1) / TOTAL_ADS) * 100;

        progressBar.style.width = percent + "%";

        step.innerText = currentAd <= TOTAL_ADS ? currentAd : TOTAL_ADS;

    }

    for (let i = 1; i <= TOTAL_ADS; i++) {

        const btn = document.getElementById("btn" + i);

        if (!btn) continue;

        btn.onclick = async function () {

            if (i !== currentAd) return;

            // TODO:
            // Yaha SmartLink open hoga
            // window.open(SMARTLINKS[i-1], "_blank");

            const res = await fetch("/api/watch-ad", {

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
            btn.classList.remove("active-btn");
            btn.classList.add("complete-btn");
            btn.innerHTML = "✅ Completed";

            currentAd++;

            updateProgress();

            if (currentAd <= TOTAL_ADS) {

                const nextBtn = document.getElementById("btn" + currentAd);

                if (nextBtn) {
                    nextBtn.disabled = false;
                    nextBtn.classList.remove("lock-btn");
                    nextBtn.classList.add("active-btn");
                    nextBtn.innerHTML = "▶ WATCH NOW";
                }

            } else {

                finalButton.style.display = "block";

            }

        };

    }

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
