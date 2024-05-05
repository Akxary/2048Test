export default function handlePresses(elId: string) {
    const el = document.getElementById(elId);
    // console.log(el);
    if (!el) return;
    document.addEventListener('keydown', (event) => {
        event.preventDefault();
        el.dispatchEvent(new KeyboardEvent('keydown', {key:event.key, code:event.code}));
    })

}