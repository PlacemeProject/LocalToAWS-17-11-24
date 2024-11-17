
function filterJobs() {
    const jobCards = document.querySelectorAll('.job-card'); 
    const workModeFilters = getSelectedFilters('workMode');
    const experienceFilters = getSelectedFilters('experience');
    const salaryFilters = getSelectedFilters('salary');
    const departmentFilters = getSelectedFilters('department');
    const companyTypeFilters = getSelectedFilters('companyType');
    const roleCategoryFilters = getSelectedFilters('roleCategory');
    const locationFilters = getSelectedFilters('location');

    jobCards.forEach(card => {
        const workMode = card.querySelector('.job-details').textContent.toLowerCase();
        const location = card.querySelector('.job-details').textContent.toLowerCase();

        let show = true;
        
        if (workModeFilters.length && !workModeFilters.some(filter => workMode.includes(filter))) {
            show = false;
        }
        
        if (locationFilters.length && !locationFilters.some(filter => location.includes(filter))) {
            show = false;
        }

        if (show) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

function getSelectedFilters(filterName) {
    const checkboxes = document.querySelectorAll(`input[name="${filterName}"]:checked`);
    return Array.from(checkboxes).map(checkbox => checkbox.value.toLowerCase());
}

document.querySelector('button').addEventListener('click', filterJobs);
  

function updateExperienceLabel(value) {
    const experienceLabel = document.getElementById('experienceLabel');
    const slider = document.getElementById('experienceSlider');

    // Set label text, with 20+ years if at max
    experienceLabel.textContent = value === '21' ? '20+' : `${value} `;

    // Position label above the slider thumb
    const thumbPosition = (value / 21) * 100;
    // experienceLabel.style.left = `calc(${thumbPosition}% - 10px)`;
    experienceLabel.style.left = `calc(${thumbPosition}% + 10px)`;

    // Update the background fill as the slider moves
    slider.style.setProperty('--progress', `${thumbPosition}%`);
}

function toggleView(moreOptionsId, viewMoreLinkId) {
    const moreOptions = document.getElementById(moreOptionsId);
    const viewMoreLink = document.getElementById(viewMoreLinkId);
    
    if (moreOptions.classList.contains("hidden")) {
        moreOptions.classList.remove("hidden");
        viewMoreLink.textContent = "View Less";
    } else {
        moreOptions.classList.add("hidden");
        viewMoreLink.textContent = "View More";
    }
}

function filterList() {
    const searchInput = document.querySelector('.filter-search').value.toLowerCase();
    const items = document.querySelectorAll('.filter-item');

    items.forEach(item => {
      const label = item.textContent.toLowerCase();
      if (label.includes(searchInput)) {
        item.style.display = 'flex';
      } else {
        item.style.display = 'none';
      }
    });
  }