document.addEventListener('DOMContentLoaded', () => {
  const body = document.body;
  const loader = document.getElementById('loader');
  const backToTopButton = document.getElementById('back-to-top');
  const nav = document.getElementById('primary-navigation');
  const navToggle = document.querySelector('.nav-toggle');
  const navLinks = Array.from(document.querySelectorAll('.nav-link'));
  const revealElements = Array.from(document.querySelectorAll('.reveal'));
  const filterButtons = Array.from(document.querySelectorAll('.filter-btn'));
  const galleryCards = Array.from(document.querySelectorAll('.gallery-card'));
  const projectCount = document.getElementById('project-count');
  const contactForm = document.getElementById('contact-form');
  const formStatus = document.getElementById('form-status');
  const portraitImage = document.getElementById('portrait-image');

  const setLoaderState = () => {
    window.setTimeout(() => {
      if (loader) {
        loader.classList.add('is-hidden');
      }
      body.classList.add('is-ready');
    }, 250);
  };

  if (document.readyState === 'complete') {
    setLoaderState();
  } else {
    window.addEventListener('load', setLoaderState, { once: true });
  }

  if (portraitImage) {
    portraitImage.addEventListener('error', () => {
      portraitImage.style.display = 'none';
    });
  }

  const closeMobileNav = () => {
    if (nav) {
      nav.classList.remove('nav-open');
    }
    if (navToggle) {
      navToggle.setAttribute('aria-expanded', 'false');
    }
  };

  if (navToggle) {
    navToggle.addEventListener('click', () => {
      const isOpen = nav ? nav.classList.toggle('nav-open') : false;
      navToggle.setAttribute('aria-expanded', String(isOpen));
    });
  }

  navLinks.forEach((link) => {
    link.addEventListener('click', () => {
      closeMobileNav();
    });
  });

  const highlightNavLink = (id) => {
    navLinks.forEach((link) => {
      const target = link.getAttribute('href').slice(1);
      link.classList.toggle('active', target === id);
    });
  };

  const sectionObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          highlightNavLink(entry.target.id);
        }
      });
    },
    {
      threshold: 0.2,
      rootMargin: '0px 0px -20% 0px'
    }
  );

  revealElements.forEach((element) => sectionObserver.observe(element));

  const pageSectionObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          highlightNavLink(entry.target.id);
        }
      });
    },
    {
      threshold: 0.55,
      rootMargin: '0px 0px -30% 0px'
    }
  );

  document.querySelectorAll('section[id]').forEach((section) => pageSectionObserver.observe(section));

  const updateBackToTop = () => {
    if (!backToTopButton) return;
    if (window.scrollY > 500) {
      backToTopButton.classList.add('is-visible');
    } else {
      backToTopButton.classList.remove('is-visible');
    }
  };

  window.addEventListener('scroll', updateBackToTop, { passive: true });
  updateBackToTop();

  if (backToTopButton) {
    backToTopButton.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  const updateGalleryCount = (visibleCards) => {
    if (!projectCount) return;
    const count = visibleCards.length;
    projectCount.textContent = `Showing ${count} Project${count === 1 ? '' : 's'}`;
  };

  const setActiveFilter = (filter) => {
    filterButtons.forEach((button) => {
      button.classList.toggle('active', button.dataset.filter === filter);
    });
  };

  const filterGallery = (filter) => {
    let visibleCards = [];

    galleryCards.forEach((card) => {
      const categories = (card.dataset.category || '').split(' ');
      const isVisible = filter === 'all' || categories.includes(filter);

      card.classList.toggle('is-hidden', !isVisible);
      if (isVisible) {
        visibleCards.push(card);
      }
    });

    updateGalleryCount(visibleCards);
  };

  filterButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const filter = button.dataset.filter;

      setActiveFilter(filter);
      filterGallery(filter);
    });
  });

  document.querySelectorAll('.blog-toggle').forEach((button) => {
    button.addEventListener('click', () => {
      const card = button.closest('.blog-card');
      const content = card?.querySelector('.blog-card__expanded');
      if (!card || !content) return;

      const expanded = card.classList.toggle('is-expanded');
      button.textContent = expanded ? 'Read Less' : 'Read More';
      button.setAttribute('aria-expanded', String(expanded));
      content.setAttribute('aria-hidden', String(!expanded));

      if (expanded) {
        content.style.display = 'block';
        content.style.overflow = 'hidden';
        content.style.opacity = '1';
        content.style.maxHeight = '0';
        window.requestAnimationFrame(() => {
          content.style.maxHeight = `${content.scrollHeight}px`;
        });
      } else {
        content.style.maxHeight = '0';
        content.style.opacity = '0';
      }
    });
  });

  highlightNavLink('hero');
  setActiveFilter('all');
  filterGallery('all');

  if (contactForm && formStatus) {
    contactForm.addEventListener('submit', (event) => {
      event.preventDefault();

      const formData = new FormData(contactForm);
      const name = String(formData.get('name') || '').trim();

      if (!name) {
        formStatus.textContent = 'Please enter your name before sending the message.';
        formStatus.style.color = 'var(--accent)';
        return;
      }

      formStatus.textContent = 'Thanks. Your message is ready to be connected to a backend or email service later.';
      formStatus.style.color = 'var(--success)';
      contactForm.reset();
    });
  }
});
