function readURL(input, elem) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            const subBtn = $("#submit-btn");
            subBtn.removeClass('disabled');

            const tieElem = $(`#${elem}`);
            tieElem.attr("src", e.target.result);
            tieElem.css('visibility', 'visible');
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function sleep(time) {
    return new Promise((resolve) => setTimeout(resolve, time));
}

async function deleteTiePoint(id) {
    data = new FormData();
    data.append('tie_point_id', id);

    let request = new XMLHttpRequest();
    request.open("POST", 'tie_points', true);
    request.send(data);
    await sleep(1800);
    location.reload();
}