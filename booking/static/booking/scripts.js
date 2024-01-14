document.addEventListener('DOMContentLoaded', function() {
    loadCars();
    loadRentalHistory();
    document.getElementById('rental-form').addEventListener('submit', handleRentalFormSubmit);
});

carNames = {}

function loadCars() {
    fetch('http://127.0.0.1:8000/api/cars/')
        .then(response => response.json())
        .then(cars => {
            const select = document.getElementById('car-select');
            cars.forEach(car => {
                const option = document.createElement('option');
                option.value = car.id;
                option.textContent = `${car.make} ${car.model} - ${car.year}`;
                select.appendChild(option);
                carNames[car.id] = `${car.make} ${car.model} - ${car.year} (${car.id})`
            });
        });
}

function handleRentalFormSubmit(event) {
    event.preventDefault();
    const carId = document.getElementById('car-select').value;
    const startTime = document.getElementById('start-time').value;
    const endTime = document.getElementById('end-time').value;

    fetch('http://127.0.0.1:8000/api/bookings/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ carId, startTime, endTime }),
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Failed to rent a car: ' + data.error);
        } else {
            loadRentalHistory();
        }
    });
}

let currentPage = 1;
let entriesPerPage = 10;
let paginatedHistory = [];

function loadRentalHistory() {
    clearRentalHistory()
    fetch('http://127.0.0.1:8000/api/bookings/', {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => response.json())
    .then(bookings => {
        // Split the bookings array into pages
        paginatedHistory = paginateArray(bookings.reverse(), entriesPerPage);
        if (paginatedHistory.length !== 0) displayPage(currentPage);
    })
    .catch(error => {
        console.error('Error loading rental history:', error);
    });
}

function paginateArray(array, pageSize) {
    return array.reduce((acc, item, index) => {
        const pageIndex = Math.floor(index / pageSize);
        if(!acc[pageIndex]) {
            acc[pageIndex] = [];
        }
        acc[pageIndex].push(item);
        return acc;
    }, []);
}

function clearRentalHistory() {
    const tableBody = document.getElementById('history-table').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = '';
}

function displayPage(page) {
    clearRentalHistory()
    
    const tableBody = document.getElementById('history-table').getElementsByTagName('tbody')[0];

    const pageData = paginatedHistory[page - 1];

    pageData.forEach(booking => {
        const row = tableBody.insertRow();
        row.insertCell().textContent = carNames[booking.car_id];
        row.insertCell().textContent = formatDate(new Date(booking.startTime));
        row.insertCell().textContent = formatDate(new Date(booking.endTime));
        row.insertCell().textContent = booking.status;
    });

    // Update the current page display
    document.getElementById('current-page').textContent = page;
}

function changePage(newPage) {
    newPage = Math.max(Math.min(newPage, paginatedHistory.length), 1)
    currentPage = newPage;
    displayPage(currentPage);
}

function gotoPage() {
    const page = parseInt(document.getElementById('page-input').value)
    changePage(page);
}

function formatDate(date) {
    return date.toLocaleString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric', 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}
