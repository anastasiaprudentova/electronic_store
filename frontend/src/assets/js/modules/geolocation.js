export async function requestGeolocation() {
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
        reject(new Error('Геолокация не поддерживается браузером'));
        return;
        }
        navigator.geolocation.getCurrentPosition(
        async (position) => {
            const { latitude, longitude } = position.coords;
            try {
            const response = await fetch(
                `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`
            );
            const data = await response.json();
            const city = data.address?.city || data.address?.town || data.address?.village || 'неизвестный город';
            resolve(city);
            } catch {
            reject(new Error('Город не определён'));
            }
        },
        () => {
            reject(new Error('Доступ к геолокации запрещён'));
        }
        );
    });
}