let ablePlayerInstance;
let observer;
let observerDisconnectCalled = false;
const csrf_token = Cookies.get('csrftoken');
const ABLE_TIMER_CLASS = 'able-elapsedTime';
const ENDED_STATE = 'ended';
const $videoScore = $("#video-score");


const addPointsPerElapsedTime = (achieved_points) => {
    let data = {
        achieved_points: achieved_points,
    }
    $.ajax({
        method: 'post',
        async: false,
        url: redeem_points_url,
        headers: {
            'X-CSRFToken': csrf_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        dataType: "json",
        data: JSON.stringify(data),
        success: function (data) {
            const {redirect_url} = data;
            window.location = redirect_url;
        }
    });
}

const observerPlayerCallBack = (mutationList) => {
    mutationList.forEach((mutation) => {
        if (mutation.type === 'childList') {
            let $JqueryTarget = $(mutation.target);
            if ($JqueryTarget.attr('class') === ABLE_TIMER_CLASS) {
                let elapsed = ablePlayerInstance.elapsed;
                let achieved_points = Math.floor(elapsed / 60) || 0;
                $videoScore.text(achieved_points);
                ablePlayerInstance.getPlayerState().then(state => {
                    if (state === ENDED_STATE && observerDisconnectCalled === false) {
                        observerDisconnectCalled = true;
                        observer.disconnect();
                        addPointsPerElapsedTime(achieved_points);
                    }
                })
            }
        }
    })
}

$(function () {
    ablePlayerInstance = window.AblePlayerInstances[0];
    let player = $('#player');

    observer = new MutationObserver(observerPlayerCallBack);
    observer.observe(player.get(0), {childList: true, attributes: true, characterData: true, subtree: true});
    const $redeemPointsEarly = $('#redeem-points-early');
    $redeemPointsEarly.click(() => {
        observer.disconnect();
        let elapsed = ablePlayerInstance.elapsed;
        let achieved_points = Math.floor(elapsed / 60) || 0;
        addPointsPerElapsedTime(achieved_points);
    })
});