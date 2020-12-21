const form = document.getElementById("form");
const urls_shortened = document.getElementById("urls-shortened");
const urls_shortened_card = document.getElementById("urls-shortened-card");

function on_form_submit() {
    $.ajax({
        type: "post",
        url: "/add_link/",
        data: $(form).serializeObject(),

        success: function (data, text) {
            qrcode_url = new QRious({
                value: `http://${host}/${data.short_link_ending}`
              }).toDataURL();
            
            urls_shortened_card.style.setProperty("visibility", "visible");

            urls_shortened.innerHTML = urls_shortened.innerHTML + `
            <article class="message mb-2">
                <div class="message-body">
                <nav class="level">
                    <div class="level-left">
                        <div class="level-item">
                            <div>
                                <p><a href="http://${host}/${data.short_link_ending}" target="_blank" class="is-size-5">http://${host}/${data.short_link_ending}</a></p>
                                <p>Goes to ${data.long_url}<p>
                            </div>
                        </div>
                    </div>

                    <div class="level-right">
                        <a data-tooltip="Click on me to download the QR Code" class="level-item has-tooltip-left has-tooltip-arrow" href=${qrcode_url} download>
                            <img src=${qrcode_url} height=${urls_shortened.offsetHeight}>
                        </a>
                    </div>
                </div>
            </article>
            `;
        },

        error: function (request, status, error) {
            bulmaToast.toast({
				message: request.responseJSON.error,
				type: 'is-danger',
				duration: 3500,
				dismissible: true,
			});
        }
    });

    hcaptcha.reset();
}


function elementHasChildren(element) {
	/*
	Checks if element has children safely
	Whats unique about this is that it strips
	comments and whitespace, so it won't count
	those as children
	*/

	element.innerHTML = element.innerHTML.trim(); // Strip whitespace
	element.innerHTML = element.innerHTML.replace(/<\!--.*?-->/g, ""); // Strip HTML comments

	return element.innerHTML.trim() !== '';
}