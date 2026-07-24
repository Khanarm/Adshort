document.addEventListener("DOMContentLoaded", function () {

    const planButtons = document.querySelectorAll(".plan-btn");
    const selectedAds = document.getElementById("selectedAds");
    const selectedCpm = document.getElementById("selectedCpm");
    const adsInput = document.getElementById("adsInput");
    const cpmInput = document.getElementById("cpmInput");

    if (planButtons.length > 0) {

        planButtons[0].classList.remove("btn-outline-primary");
        planButtons[0].classList.add("btn-primary");

        planButtons.forEach(button => {

            button.addEventListener("click", function () {

                planButtons.forEach(btn => {
                    btn.classList.remove("btn-primary");
                    btn.classList.add("btn-outline-primary");
                });

                this.classList.remove("btn-outline-primary");
                this.classList.add("btn-primary");

                selectedAds.textContent = this.dataset.ads + " Ads";
                selectedCpm.textContent = "$" + this.dataset.cpm;

                adsInput.value = this.dataset.ads;
                cpmInput.value = this.dataset.cpm;

            });

        });

    }

});
