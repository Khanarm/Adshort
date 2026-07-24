document.addEventListener("DOMContentLoaded", function () {

    // =========================
    // Plan Selection
    // =========================

    const planButtons = document.querySelectorAll(".plan-btn");
    const selectedAds = document.getElementById("selectedAds");
    const selectedCpm = document.getElementById("selectedCpm");
    const adsHidden = document.getElementById("adsHidden");
    const cpmHidden = document.getElementById("cpmHidden");

    if (planButtons.length > 0) {

        // Default Selected Plan
        planButtons[0].classList.remove("btn-outline-primary");
        planButtons[0].classList.add("btn-primary");

        if (selectedAds) {
            selectedAds.textContent = "1 Ads";
        }

        if (selectedCpm) {
            selectedCpm.textContent = "$0.50";
        }

        if (adsHidden) {
            adsHidden.value = "1";
        }

        if (cpmHidden) {
            cpmHidden.value = "0.50";
        }

        // Change Plan
        planButtons.forEach(button => {

            button.addEventListener("click", function () {

                planButtons.forEach(btn => {
                    btn.classList.remove("btn-primary");
                    btn.classList.add("btn-outline-primary");
                });

                this.classList.remove("btn-outline-primary");
                this.classList.add("btn-primary");

                const ads = this.dataset.ads;
                const cpm = this.dataset.cpm;

                if (selectedAds) {
                    selectedAds.textContent = ads + " Ads";
                }

                if (selectedCpm) {
                    selectedCpm.textContent = "$" + cpm;
                }

                if (adsHidden) {
                    adsHidden.value = ads;
                }

                if (cpmHidden) {
                    cpmHidden.value = cpm;
                }

            });

        });

    }

    // =========================
    // Copy Generated Link
    // =========================

    const copyButton = document.querySelector(".copy-btn");

    if (copyButton) {

        copyButton.addEventListener("click", function () {

            const link = this.dataset.link;

            navigator.clipboard.writeText(link).then(() => {

                const originalText = this.innerHTML;

                this.innerHTML = "✅ Copied!";
                this.classList.remove("btn-light");
                this.classList.add("btn-success");

                setTimeout(() => {

                    this.innerHTML = '<i class="bi bi-clipboard"></i> Copy Link';
                    this.classList.remove("btn-success");
                    this.classList.add("btn-light");

                }, 2000);

            });

        });

    }

});
