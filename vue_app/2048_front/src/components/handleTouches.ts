export default function handleTouches(elId: string) {
    const el = document.getElementById(elId);
    console.log(el);
    if (el == null)
        return;
    el.addEventListener('touchstart', handleTouchStart, {passive: false});
    el.addEventListener('touchmove', handleTouchMove, {passive: false});

    let xDown: number | null = null;
    let yDown: number | null = null;

    function getTouches(evt: TouchEvent) {
        return evt.touches// browser API
    }

    function handleTouchStart(evt: TouchEvent) {
        // evt.preventDefault();
        const firstTouch = getTouches(evt)[0];
        xDown = firstTouch.clientX;
        yDown = firstTouch.clientY;
    }

    function handleTouchMove(evt: TouchEvent) {
        evt.preventDefault();
        if (!xDown || !yDown) {
            return;
        }

        const xUp = evt.touches[0].clientX;
        const yUp = evt.touches[0].clientY;

        const xDiff: number = xDown - xUp;
        const yDiff: number = yDown - yUp;

        if (Math.abs(xDiff) > Math.abs(yDiff)) {/*most significant*/
            if (xDiff > 0) {
                /* left swipe */
                console.log("swipe left");
                console.log("dispath swipe left");
                if (el)
                    el.dispatchEvent(new KeyboardEvent('keydown', {key: 'ArrowLeft', code: 'ArrowLeft'}));
            } else {
                /* right swipe */
                console.log("swipe right");
                if (el)
                    el.dispatchEvent(new KeyboardEvent('keydown', {key: 'ArrowRight', code: 'ArrowRight'}));
            }
        } else {
            if (yDiff > 0) {
                /* up swipe */
                console.log("swipe up");
                if (el)
                    el.dispatchEvent(new KeyboardEvent('keydown', {key: 'ArrowUp', code: 'ArrowUp'}));
            } else {
                /* down swipe */
                console.log("swipe down");
                if (el)
                    el.dispatchEvent(new KeyboardEvent('keydown', {key: 'ArrowDown', code: 'ArrowDown'}));

            }
        }
        /* reset values */
        xDown = null;
        yDown = null;
    }
}
