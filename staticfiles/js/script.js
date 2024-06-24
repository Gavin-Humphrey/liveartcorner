document.addEventListener('DOMContentLoaded', function() {
    var menuIcon = document.querySelector('.menu-icon');
    var menu = document.querySelector('.menu');
    
    menuIcon.addEventListener('click', function() {
      menu.classList.toggle('show');
    });
  });

document.querySelector('.cart-icon a').addEventListener('click', function(event) {
  event.stopPropagation(); // Prevents click event from bubbling to the menu-icon
});

document.addEventListener('DOMContentLoaded', function() {
  var cartIcon = document.getElementById('cart-icon-wrapper');
  
  cartIcon.addEventListener('click', function() {
      window.location.href = "{% url 'view_cart' %}";
  });
});

  
// Card container and slide
document.addEventListener("DOMContentLoaded", function() {
  const cards = document.querySelectorAll('.card');

  cards.forEach(card => {
    let currentItem = 0;
    const items = card.querySelector('.card-items-wrapper');
    const totalItems = card.querySelectorAll('.card-item').length;

    function updateItemWidth() {
      const itemWidth = card.querySelector('.card-item').offsetWidth;
      return itemWidth;
    }

    card.querySelectorAll('.card-item img').forEach(img => {
      img.addEventListener('load', updateItemWidth);
    });

    card.querySelector('.prev').addEventListener('click', function() {
      if (currentItem > 0) {
        currentItem--;
        items.style.transform = `translateX(-${updateItemWidth() * currentItem}px)`;
      }
    });

    card.querySelector('.next').addEventListener('click', function() {
      if (currentItem < totalItems - 1) {
        currentItem++;
        items.style.transform = `translateX(-${updateItemWidth() * currentItem}px)`;
      }
    });
  });
});


   


