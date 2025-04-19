// Store user data
let userData = {
    username: "",
    coins: 100,
    points: 0,
    pets: {
        default: {
            name: "Default Pet",
            image: "images/default-pet.png",
            active: true
        },
        Monkey: {
            name: "Monkey Pet",
            image: "images/monkey-pet.png",
            price: 200,
            locked: false,
            active: true
        },
        Porcupine: {
            name: "Porcupine Pet",
            image: "images/porcupine-pet.png",
            price: 300,
            locked: false,
            active: true
        },
        Owl: {
            name: "Owl Pet",
            image: "images/owl-pet.png",
            price: 500,
            locked: false,
            active: true
        }
    },
    workouts: {
        weightlifting: [],
        stretching: [],
        cardio: []
    }
};

// Check if user data exists in local storage
function initializeApp() {
    const storedData = localStorage.getItem('fitPetUserData');
    if (storedData) {
        userData = JSON.parse(storedData);
        updateUI();
    }
}

// Save user data to local storage
function saveUserData() {
    localStorage.setItem('fitPetUserData', JSON.stringify(userData));
}

// Update UI elements with current data
function updateUI() {
    // Update coin and point counts
    const coinCountElements = document.querySelectorAll('#coin-count');
    const pointsCountElements = document.querySelectorAll('#points-count');
    
    coinCountElements.forEach(element => {
        element.textContent = userData.coins;
    });
    
    pointsCountElements.forEach(element => {
        element.textContent = userData.points;
    });
    
    // Update active pet if on dashboard
    const activePetImage = document.getElementById('active-pet');
    const petName = document.getElementById('pet-name');
    
    if (activePetImage && petName) {
        const activePet = Object.values(userData.pets).find(pet => pet.active);
        if (activePet) {
            activePetImage.src = activePet.image;
            petName.textContent = activePet.name;
        }
    }
    
    // Update workout lists if on dashboard
    updateWorkoutLists();
    
    // Update pets grid if on pets page
    updatePetsGrid();
}

// Update workout lists
function updateWorkoutLists() {
    const categories = ['weightlifting', 'stretching', 'cardio'];
    
    categories.forEach(category => {
        const listElement = document.getElementById(`${category}-list`);
        if (!listElement) return;
        
        // Clear existing list
        listElement.innerHTML = '';
        
        // Add workouts to list
        userData.workouts[category].forEach((workout, index) => {
            const li = document.createElement('li');
            li.innerHTML = `
                <span>${workout.name}</span>
                <div>
                    <input type="checkbox" id="${category}-${index}" 
                        ${workout.completed ? 'checked' : ''}>
                    <button class="delete-btn" data-category="${category}" data-index="${index}">❌</button>
                </div>
            `;
            
            if (workout.completed) {
                li.classList.add('completed');
            }
            
            listElement.appendChild(li);
            
            // Add event listener to checkbox
            const checkbox = document.getElementById(`${category}-${index}`);
            if (checkbox) {
                checkbox.addEventListener('change', (e) => {
                    toggleWorkoutCompletion(category, index);
                });
            }
        });
    });
    
    // Add event listeners to delete buttons
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const category = e.target.dataset.category;
            const index = parseInt(e.target.dataset.index);
            deleteWorkout(category, index);
        });
    });
}

// Add a new workout
function addWorkout(category, workoutName) {
    if (!workoutName.trim()) return;
    
    userData.workouts[category].push({
        name: workoutName,
        completed: false,
        dateAdded: new Date().toISOString()
    });
    
    saveUserData();
    updateWorkoutLists();
}

// Toggle workout completion status
function toggleWorkoutCompletion(category, index) {
    userData.workouts[category][index].completed = !userData.workouts[category][index].completed;
    
    // Award coins for completed workout
    if (userData.workouts[category][index].completed) {
        userData.coins += 10;
        userData.points += 5;
    } else {
        userData.coins -= 10;
        userData.points -= 5;
    }
    
    saveUserData();
    updateUI();
}

// Delete a workout
function deleteWorkout(category, index) {
    userData.workouts[category].splice(index, 1);
    saveUserData();
    updateWorkoutLists();
}

// Update pets grid
function updatePetsGrid() {
    const petsGrid = document.querySelector('.pets-grid');
    if (!petsGrid) return;
    
    // Clear existing grid
    petsGrid.innerHTML = '';
    
    // Add pets to grid
    Object.entries(userData.pets).forEach(([id, pet]) => {
        const petCard = document.createElement('div');
        petCard.className = `pet-card ${pet.locked ? 'locked' : ''} ${pet.active ? 'active' : ''}`;
        petCard.dataset.id = id;
        
        // Always show the pet image, even if locked
        petCard.innerHTML = `
            <img src="${pet.image}" alt="${pet.name}">
            <h3>${pet.name}</h3>
        `;
        
        if (pet.locked) {
            // Add lock overlay but keep the pet image visible
            const lockOverlay = document.createElement('div');
            lockOverlay.className = 'lock-overlay';
            lockOverlay.innerHTML = `<img src="images/lock.png" alt="Locked" class="lock-icon">`;
            petCard.appendChild(lockOverlay);
            
            // Add price and unlock button
            const priceElement = document.createElement('p');
            priceElement.className = 'pet-price';
            priceElement.textContent = `${pet.price} coins`;
            petCard.appendChild(priceElement);
            
            const unlockButton = document.createElement('button');
            unlockButton.className = 'buy-btn';
            unlockButton.dataset.id = id;
            unlockButton.dataset.price = pet.price;
            unlockButton.textContent = 'Unlock';
            petCard.appendChild(unlockButton);
        } else {
            // Add status and select button
            const statusElement = document.createElement('p');
            statusElement.textContent = pet.active ? 'Currently Active' : '';
            petCard.appendChild(statusElement);
            
            const selectButton = document.createElement('button');
            selectButton.className = `select-btn ${pet.active ? 'selected' : ''}`;
            selectButton.dataset.id = id;
            selectButton.textContent = pet.active ? 'Selected' : 'Select';
            petCard.appendChild(selectButton);
        }
        
        petsGrid.appendChild(petCard);
    });
    
    // Add event listeners to buttons
    document.querySelectorAll('.select-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            selectPet(e.target.dataset.id);
        });
    });
    
    document.querySelectorAll('.buy-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            buyPet(e.target.dataset.id, parseInt(e.target.dataset.price));
        });
    });
}

// Select a pet as active
function selectPet(petId) {
    // Deactivate all pets
    Object.keys(userData.pets).forEach(id => {
        userData.pets[id].active = false;
    });
    
    // Activate selected pet
    userData.pets[petId].active = true;
    
    saveUserData();
    updateUI();
}

// Buy a new pet
function buyPet(petId, price) {
    if (userData.coins >= price) {
        userData.coins -= price;
        userData.pets[petId].locked = false;
        
        saveUserData();
        updateUI();
        
        alert(`You've successfully unlocked ${userData.pets[petId].name}!`);
    } else {
        alert(`Not enough coins! You need ${price - userData.coins} more coins.`);
    }
}

// Event listeners for login page
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    
    // Login/Signup buttons
    const loginBtn = document.getElementById('login-btn');
    const signupBtn = document.getElementById('signup-btn');
    
    if (loginBtn) {
        loginBtn.addEventListener('click', () => {
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            if (username && password) {
                userData.username = username;
                saveUserData();
                window.location.href = 'dashboard.html';
            } else {
                alert('Please enter username and password');
            }
        });
    }
    
    if (signupBtn) {
        signupBtn.addEventListener('click', () => {
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            if (username && password) {
                userData.username = username;
                saveUserData();
                window.location.href = 'dashboard.html';
            } else {
                alert('Please enter username and password');
            }
        });
    }
    
    // Add workout buttons
    const addButtons = document.querySelectorAll('.add-btn');
    addButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const category = e.target.dataset.category;
            const inputElement = document.getElementById(`${category}-input`);
            
            if (inputElement) {
                addWorkout(category, inputElement.value);
                inputElement.value = '';
            }
        });
    });
    
    // Show prices button
    const showPricesBtn = document.getElementById('show-prices');
    if (showPricesBtn) {
        showPricesBtn.addEventListener('click', () => {
            alert('Pet Prices:\n' + 
                  Object.entries(userData.pets)
                      .filter(([_, pet]) => pet.price)
                      .map(([_, pet]) => `${pet.name}: ${pet.price} coins`)
                      .join('\n'));
        });
    }
});

