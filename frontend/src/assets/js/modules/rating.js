export function renderRating(rating = 0, reviews = 0) {
    const fullStars = Math.floor(rating);
    const hasHalf = rating % 1 >= 0.5;
    const emptyStars = 5 - fullStars - (hasHalf ? 1 : 0);
    
    let starsHtml = '';
    for (let i = 0; i < fullStars; i++) {
        starsHtml += '<i class="fa-solid fa-star"></i>';
    }
    if (hasHalf) {
        starsHtml += '<i class="fa-solid fa-star-half-alt"></i>';
    }
    for (let i = 0; i < emptyStars; i++) {
        starsHtml += '<i class="fa-regular fa-star"></i>';
    }
    
    const reviewsText = reviews === 1 ? 'отзыв' : 'отзывов';
    return `
        <div class="rating">
        ${starsHtml}
        <span class="rating-value">${rating.toFixed(1)}</span>
        <span class="reviews-count">(${reviews} ${reviewsText})</span>
        </div>
    `;
}