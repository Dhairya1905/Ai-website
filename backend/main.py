from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import json
import uuid
from datetime import datetime

app = FastAPI(title="AI Website Generator API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class WebsiteRequest(BaseModel):
    prompt: str
    template: Optional[str] = None
    style: Optional[str] = "modern"

class WebsiteResponse(BaseModel):
    id: str
    html: str
    css: str
    js: str
    metadata: Dict[str, Any]

# In-memory storage (replace with database in production)
projects = {}

# Component templates
COMPONENTS = {
    "navbar": """
<nav class="navbar">
    <div class="nav-container">
        <div class="nav-logo">
            <h1>{{company_name}}</h1>
        </div>
        <ul class="nav-menu">
            <li class="nav-item"><a href="#home">Home</a></li>
            <li class="nav-item"><a href="#about">About</a></li>
            <li class="nav-item"><a href="#services">Services</a></li>
            <li class="nav-item"><a href="#contact">Contact</a></li>
        </ul>
    </div>
</nav>
""",
    "hero": """
<section class="hero" id="home">
    <div class="hero-content">
        <h1>{{headline}}</h1>
        <p>{{subheadline}}</p>
        <button class="cta-button">{{cta_text}}</button>
    </div>
</section>
""",
    "about": """
<section class="about" id="about">
    <div class="container">
        <h2>About Us</h2>
        <p>{{about_text}}</p>
    </div>
</section>
""",
    "contact": """
<section class="contact" id="contact">
    <div class="container">
        <h2>Contact Us</h2>
        <form class="contact-form">
            <input type="text" placeholder="Name" required>
            <input type="email" placeholder="Email" required>
            <textarea placeholder="Message" required></textarea>
            <button type="submit">Send Message</button>
        </form>
    </div>
</section>
"""
}

# Base CSS styles
BASE_CSS = """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: #333;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Navbar Styles */
.navbar {
    background: #fff;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 1000;
}

.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 70px;
}

.nav-logo h1 {
    color: #2563eb;
    font-size: 1.8rem;
}

.nav-menu {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-item a {
    text-decoration: none;
    color: #333;
    font-weight: 500;
    transition: color 0.3s;
}

.nav-item a:hover {
    color: #2563eb;
}

/* Hero Section */
.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 150px 0 100px;
    text-align: center;
}

.hero-content h1 {
    font-size: 3.5rem;
    margin-bottom: 1rem;
    font-weight: 700;
}

.hero-content p {
    font-size: 1.3rem;
    margin-bottom: 2rem;
    opacity: 0.9;
}

.cta-button {
    background: #fff;
    color: #667eea;
    padding: 15px 30px;
    border: none;
    border-radius: 50px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.3s, box-shadow 0.3s;
}

.cta-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

/* About Section */
.about {
    padding: 100px 0;
    background: #f8f9fa;
}

.about h2 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 3rem;
    color: #1a1a1a;
}

.about p {
    text-align: center;
    font-size: 1.1rem;
    max-width: 800px;
    margin: 0 auto;
    line-height: 1.8;
    color: #4a4a4a;
}

/* Contact Section */
.contact {
    padding: 100px 0;
    background: #ffffff;
}

.contact h2 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 3rem;
    color: #1a1a1a;
}

.contact-form {
    max-width: 600px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.contact-form input,
.contact-form textarea {
    padding: 15px;
    border: 2px solid #e5e7eb;
    border-radius: 8px;
    font-size: 1rem;
    color: #333;
    background: #ffffff;
}

.contact-form input::placeholder,
.contact-form textarea::placeholder {
    color: #9ca3af;
}

.contact-form input:focus,
.contact-form textarea:focus {
    outline: none;
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.contact-form button {
    background: #2563eb;
    color: white;
    padding: 15px;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    cursor: pointer;
    transition: background 0.3s;
}

.contact-form textarea {
    min-height: 150px;
    resize: vertical;
}

.contact-form button:hover {
    background: #1d4ed8;
}

/* Responsive Design */
@media (max-width: 768px) {
    .nav-menu {
        flex-direction: column;
        position: fixed;
        left: -100%;
        top: 70px;
        gap: 0;
        background: white;
        width: 100%;
        text-align: center;
        transition: 0.3s;
        box-shadow: 0 10px 27px rgba(0,0,0,0.05);
        padding: 2rem 0;
    }
    
    .hero-content h1 {
        font-size: 2.5rem;
    }
    
    .hero-content p {
        font-size: 1.1rem;
    }
    
    .about h2,
    .contact h2 {
        font-size: 2rem;
        color: #1a1a1a;
    }
}
"""

def generate_website_content(prompt: str, template: str = None) -> dict:
    """Generate website content based on prompt using AI-like logic"""
    
    # Analyze prompt for specific requirements
    prompt_lower = prompt.lower()
    
    # Base content
    content = {
        "company_name": "Your Company",
        "headline": "Welcome to Our Website",
        "subheadline": "We create amazing digital experiences",
        "cta_text": "Get Started",
        "about_text": "We are a passionate team dedicated to delivering excellence in everything we do."
    }
    
    # Detailed photography portfolio analysis
    if "photography" in prompt_lower and "portfolio" in prompt_lower:
        content.update({
            "company_name": "Photography Portfolio",
            "headline": "Capturing Life's Beautiful Moments",
            "subheadline": "Award-winning photography from around the world",
            "cta_text": "View Portfolio",
            "about_text": "With over 10 years of experience, I specialize in capturing the essence of our world through my lens. From breathtaking landscapes to intimate street moments, every photograph tells a unique story.",
            "gallery_categories": "Travel, Nature, Street, Aerial",
            "services_title": "Photography Services",
            "services_text": "Professional photography services for weddings, events, commercial projects, and fine art commissions."
        })
        
        # Add specific sections based on prompt requirements
        if "travel" in prompt_lower:
            content["travel_section"] = """
<section class="travel-gallery">
    <div class="container">
        <h2>Travel Photography</h2>
        <p>Journey through captivating destinations around the globe</p>
        <div class="gallery-grid">
            <div class="gallery-item">
                <img src="https://picsum.photos/seed/travel1/400/300.jpg" alt="Travel Photography">
                <div class="gallery-overlay">
                    <h3>Sunset at Santorini</h3>
                    <p>Greece, 2024</p>
                </div>
            </div>
            <div class="gallery-item">
                <img src="https://picsum.photos/seed/travel2/400/300.jpg" alt="Travel Photography">
                <div class="gallery-overlay">
                    <h3>Morning Mist in Kyoto</h3>
                    <p>Japan, 2024</p>
                </div>
            </div>
        </div>
    </div>
</section>
"""
        
        if "nature" in prompt_lower:
            content["nature_section"] = """
<section class="nature-gallery">
    <div class="container">
        <h2>Nature Photography</h2>
        <p>Exploring the beauty of the natural world</p>
        <div class="gallery-grid">
            <div class="gallery-item">
                <img src="https://picsum.photos/seed/nature1/400/300.jpg" alt="Nature Photography">
                <div class="gallery-overlay">
                    <h3>Mountain Sunrise</h3>
                    <p>Swiss Alps, 2024</p>
                </div>
            </div>
            <div class="gallery-item">
                <img src="https://picsum.photos/seed/nature2/400/300.jpg" alt="Nature Photography">
                <div class="gallery-overlay">
                    <h3>Forest Path</h3>
                    <p>Black Forest, Germany</p>
                </div>
            </div>
        </div>
    </div>
</section>
"""
        
        if "street" in prompt_lower:
            content["street_section"] = """
<section class="street-gallery">
    <div class="container">
        <h2>Street Photography</h2>
        <p>Capturing life as it happens in urban environments</p>
        <div class="gallery-grid">
            <div class="gallery-item">
                <img src="https://picsum.photos/seed/street1/400/300.jpg" alt="Street Photography">
                <div class="gallery-overlay">
                    <h3>Rush Hour</h3>
                    <p>Tokyo, Japan</p>
                </div>
            </div>
            <div class="gallery-item">
                <img src="https://picsum.photos/seed/street2/400/300.jpg" alt="Street Photography">
                <div class="gallery-overlay">
                    <h3>Cafe Life</h3>
                    <p>Paris, France</p>
                </div>
            </div>
        </div>
    </div>
</section>
"""
        
        if "aerial" in prompt_lower:
            content["aerial_section"] = """
<section class="aerial-gallery">
    <div class="container">
        <h2>Aerial Photography</h2>
        <p>Seeing the world from a different perspective</p>
        <div class="gallery-grid">
            <div class="gallery-item">
                <img src="https://picsum.photos/seed/aerial1/400/300.jpg" alt="Aerial Photography">
                <div class="gallery-overlay">
                    <h3>Coastal Patterns</h3>
                    <p>California Coast</p>
                </div>
            </div>
            <div class="gallery-item">
                <img src="https://picsum.photos/seed/aerial2/400/300.jpg" alt="Aerial Photography">
                <div class="gallery-overlay">
                    <h3>City Lights</h3>
                    <p>New York City</p>
                </div>
            </div>
        </div>
    </div>
</section>
"""
    
    # E-commerce with jewelry
    elif "ecommerce" in prompt_lower and "jewelry" in prompt_lower:
        content.update({
            "company_name": "Artisan Jewelry Collection",
            "headline": "Handcrafted Elegance",
            "subheadline": "Unique pieces made with love and precious materials",
            "cta_text": "Shop Collection",
            "about_text": "We create unique, handcrafted jewelry pieces that tell your story and complement your style. Each piece is carefully crafted using traditional techniques and modern design.",
            "products_title": "Featured Collections",
            "products_text": "Discover our curated selection of rings, necklaces, earrings, and bracelets."
        })
    
    # Restaurant/Cafe
    elif "restaurant" in prompt_lower or "cafe" in prompt_lower:
        content.update({
            "company_name": "Gourmet Restaurant",
            "headline": "Exceptional Dining Experience",
            "subheadline": "Fresh ingredients, innovative cuisine, memorable moments",
            "cta_text": "Reserve Table",
            "about_text": "We bring you the finest culinary experience with fresh, locally-sourced ingredients and innovative recipes that celebrate both tradition and creativity.",
            "menu_title": "Our Menu",
            "menu_text": "Seasonal dishes crafted with passion and precision"
        })
    
    # Business/Corporate
    elif "business" in prompt_lower or "corporate" in prompt_lower:
        content.update({
            "company_name": "Business Solutions",
            "headline": "Innovative Business Solutions",
            "subheadline": "Driving success through technology and expertise",
            "cta_text": "Learn More",
            "about_text": "We provide cutting-edge business solutions that help companies thrive in the digital age. Our team of experts delivers results that matter.",
            "services_title": "Our Services",
            "services_text": "Comprehensive solutions for modern businesses"
        })
    
    # Modern design requirements
    if "modern" in prompt_lower or "minimal" in prompt_lower:
        content["design_style"] = "modern"
        content["color_scheme"] = "minimal"
    
    if "responsive" in prompt_lower:
        content["responsive"] = True
    
    if "seo" in prompt_lower:
        content["seo_optimized"] = True
    
    return content

def build_website(content: dict, template: str = None) -> dict:
    """Build complete website from content and components"""
    
    # Build HTML
    html_components = []
    
    # Add navbar
    navbar_html = COMPONENTS["navbar"]
    for key, value in content.items():
        if isinstance(value, str):
            navbar_html = navbar_html.replace(f"{{{{{key}}}}}", value)
    html_components.append(navbar_html)
    
    # Add enhanced hero section for photography
    if "photography" in content.get("company_name", "").lower():
        hero_html = """
<section class="hero" id="home">
    <div class="hero-slider">
        <div class="hero-slide active">
            <img src="https://picsum.photos/seed/hero1/1920/1080.jpg" alt="Hero Image 1">
            <div class="hero-content">
                <h1>{headline}</h1>
                <p>{subheadline}</p>
                <button class="cta-button">{cta_text}</button>
            </div>
        </div>
        <div class="hero-slide">
            <img src="https://picsum.photos/seed/hero2/1920/1080.jpg" alt="Hero Image 2">
            <div class="hero-content">
                <h1>{headline}</h1>
                <p>{subheadline}</p>
                <button class="cta-button">{cta_text}</button>
            </div>
        </div>
        <div class="hero-slide">
            <img src="https://picsum.photos/seed/hero3/1920/1080.jpg" alt="Hero Image 3">
            <div class="hero-content">
                <h1>{headline}</h1>
                <p>{subheadline}</p>
                <button class="cta-button">{cta_text}</button>
            </div>
        </div>
    </div>
    <div class="slider-controls">
        <button class="slider-btn prev">‹</button>
        <button class="slider-btn next">›</button>
    </div>
</section>
"""
    else:
        hero_html = COMPONENTS["hero"]
    
    for key, value in content.items():
        if isinstance(value, str):
            hero_html = hero_html.replace(f"{{{{{key}}}}}", value)
    html_components.append(hero_html)
    
    # Add category sections for photography
    if content.get("travel_section"):
        html_components.append(content["travel_section"])
    
    if content.get("nature_section"):
        html_components.append(content["nature_section"])
    
    if content.get("street_section"):
        html_components.append(content["street_section"])
    
    if content.get("aerial_section"):
        html_components.append(content["aerial_section"])
    
    # Add about section
    about_html = COMPONENTS["about"]
    for key, value in content.items():
        if isinstance(value, str):
            about_html = about_html.replace(f"{{{{{key}}}}}", value)
    html_components.append(about_html)
    
    # Add services section if available
    if content.get("services_title"):
        services_html = f"""
<section class="services" id="services">
    <div class="container">
        <h2>{content.get('services_title', 'Our Services')}</h2>
        <p>{content.get('services_text', 'Professional services tailored to your needs')}</p>
        <div class="services-grid">
            <div class="service-card">
                <h3>Wedding Photography</h3>
                <p>Capturing your special day with artistic vision and attention to detail.</p>
            </div>
            <div class="service-card">
                <h3>Event Coverage</h3>
                <p>Professional documentation of corporate events, parties, and celebrations.</p>
            </div>
            <div class="service-card">
                <h3>Commercial Projects</h3>
                <p>High-quality imagery for brands, products, and marketing campaigns.</p>
            </div>
        </div>
    </div>
</section>
"""
        html_components.append(services_html)
    
    # Add contact section
    contact_html = COMPONENTS["contact"]
    for key, value in content.items():
        if isinstance(value, str):
            contact_html = contact_html.replace(f"{{{{{key}}}}}", value)
    html_components.append(contact_html)
    
    # Enhanced CSS with animations and modern design
    enhanced_css = BASE_CSS + """
/* Enhanced Hero Section with Slider */
.hero {
    position: relative;
    height: 100vh;
    overflow: hidden;
}

.hero-slider {
    position: relative;
    height: 100%;
}

.hero-slide {
    position: absolute;
    width: 100%;
    height: 100%;
    opacity: 0;
    transition: opacity 1s ease-in-out;
}

.hero-slide.active {
    opacity: 1;
}

.hero-slide img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.hero-content {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    color: white;
    z-index: 2;
    background: rgba(0,0,0,0.5);
    padding: 3rem;
    border-radius: 15px;
    backdrop-filter: blur(10px);
}

.slider-controls {
    position: absolute;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 1rem;
    z-index: 3;
}

.slider-btn {
    background: rgba(255,255,255,0.2);
    border: 2px solid white;
    color: white;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    font-size: 1.5rem;
    cursor: pointer;
    transition: all 0.3s;
}

.slider-btn:hover {
    background: rgba(255,255,255,0.3);
    transform: scale(1.1);
}

/* Enhanced Gallery Sections */
.travel-gallery, .nature-gallery, .street-gallery, .aerial-gallery {
    padding: 100px 0;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.travel-gallery h2, .nature-gallery h2, .street-gallery h2, .aerial-gallery h2 {
    text-align: center;
    font-size: 3rem;
    margin-bottom: 1rem;
    color: #1a1a1a;
}

.travel-gallery p, .nature-gallery p, .street-gallery p, .aerial-gallery p {
    text-align: center;
    font-size: 1.2rem;
    max-width: 600px;
    margin: 0 auto 4rem;
    color: #4a4a4a;
}

.gallery-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

.gallery-item {
    position: relative;
    overflow: hidden;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    transition: all 0.4s ease;
    cursor: pointer;
}

.gallery-item:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}

.gallery-item img {
    width: 100%;
    height: 300px;
    object-fit: cover;
    transition: transform 0.6s ease;
}

.gallery-item:hover img {
    transform: scale(1.1);
}

.gallery-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.9), transparent);
    color: white;
    padding: 2rem 1.5rem 1.5rem;
    transform: translateY(100%);
    transition: transform 0.4s ease;
}

.gallery-item:hover .gallery-overlay {
    transform: translateY(0);
}

.gallery-overlay h3 {
    font-size: 1.4rem;
    margin-bottom: 0.5rem;
    font-weight: 600;
}

.gallery-overlay p {
    font-size: 1rem;
    opacity: 0.9;
}

/* Lightbox Effect */
.lightbox {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.95);
    z-index: 1000;
    cursor: pointer;
}

.lightbox img {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    max-width: 90%;
    max-height: 90%;
    border-radius: 10px;
}

.lightbox-close {
    position: absolute;
    top: 20px;
    right: 40px;
    font-size: 3rem;
    color: white;
    cursor: pointer;
}

/* Enhanced Services Section */
.services {
    padding: 100px 0;
    background: #ffffff;
}

.services h2 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color: #1a1a1a;
}

.services p {
    text-align: center;
    font-size: 1.2rem;
    max-width: 600px;
    margin: 0 auto 4rem;
    color: #4a4a4a;
}

.services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

.service-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2.5rem 2rem;
    border-radius: 15px;
    text-align: center;
    color: white;
    transition: all 0.3s ease;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.service-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
}

.service-card h3 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    font-weight: 600;
}

.service-card p {
    opacity: 0.9;
    line-height: 1.6;
}

/* Smooth Animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in-up {
    animation: fadeInUp 0.8s ease-out;
}

/* Responsive Enhancements */
@media (max-width: 768px) {
    .hero-content {
        padding: 2rem 1.5rem;
        width: 90%;
    }
    
    .hero-content h1 {
        font-size: 2rem;
    }
    
    .hero-content p {
        font-size: 1rem;
    }
    
    .gallery-grid {
        grid-template-columns: 1fr;
        gap: 1.5rem;
    }
    
    .services-grid {
        grid-template-columns: 1fr;
        gap: 1.5rem;
    }
    
    .travel-gallery h2, .nature-gallery h2, .street-gallery h2, .aerial-gallery h2 {
        font-size: 2rem;
    }
}
"""
    
    # Enhanced JavaScript
    enhanced_js = """
// Hero Slider
let currentSlide = 0;
const slides = document.querySelectorAll('.hero-slide');
const totalSlides = slides.length;

function showSlide(index) {
    slides.forEach(slide => slide.classList.remove('active'));
    slides[index].classList.add('active');
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % totalSlides;
    showSlide(currentSlide);
}

function prevSlide() {
    currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
    showSlide(currentSlide);
}

// Auto-advance slider
setInterval(nextSlide, 5000);

// Slider controls
document.querySelector('.next')?.addEventListener('click', nextSlide);
document.querySelector('.prev')?.addEventListener('click', prevSlide);

// Lightbox functionality
const galleryItems = document.querySelectorAll('.gallery-item');
const lightbox = document.createElement('div');
lightbox.className = 'lightbox';
lightbox.innerHTML = '<span class="lightbox-close">&times;</span><img src="" alt="">';
document.body.appendChild(lightbox);

galleryItems.forEach(item => {
    item.addEventListener('click', function() {
        const img = this.querySelector('img');
        lightbox.style.display = 'block';
        lightbox.querySelector('img').src = img.src;
    });
});

lightbox.addEventListener('click', function() {
    this.style.display = 'none';
});

lightbox.querySelector('.lightbox-close').addEventListener('click', function(e) {
    e.stopPropagation();
    lightbox.style.display = 'none';
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Scroll animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in-up');
        }
    });
}, observerOptions);

document.querySelectorAll('section').forEach(section => {
    observer.observe(section);
});

// Form submission
document.querySelector('.contact-form')?.addEventListener('submit', function(e) {
    e.preventDefault();
    alert('Thank you for your message! We will get back to you soon.');
    this.reset();
});

// CTA button interaction
document.querySelector('.cta-button')?.addEventListener('click', function() {
    const aboutSection = document.querySelector('#about');
    if (aboutSection) {
        aboutSection.scrollIntoView({ behavior: 'smooth' });
    }
});
"""
    
    # Combine all HTML
    full_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{content.get('company_name', 'Website')}</title>
    <meta name="description" content="{content.get('subheadline', 'Professional website')}">
    <meta name="keywords" content="photography, portfolio, professional, {content.get('gallery_categories', '')}">
    <style>
{enhanced_css}
    </style>
</head>
<body>
{''.join(html_components)}
    <script>
{enhanced_js}
    </script>
</body>
</html>
"""
    
    return {
        "html": full_html,
        "css": enhanced_css,
        "js": enhanced_js
    }

@app.get("/")
async def root():
    return {"message": "AI Website Generator API"}

@app.get("/api/templates")
async def get_templates():
    """Get available website templates"""
    return {
        "templates": [
            {"id": "portfolio", "name": "Portfolio", "description": "Perfect for artists and photographers"},
            {"id": "business", "name": "Business", "description": "Professional business website"},
            {"id": "ecommerce", "name": "E-commerce", "description": "Online store template"},
            {"id": "restaurant", "name": "Restaurant", "description": "Restaurant or cafe website"},
            {"id": "custom", "name": "Custom", "description": "Generate from scratch based on your prompt"}
        ]
    }

@app.post("/api/generate", response_model=WebsiteResponse)
async def generate_website(request: WebsiteRequest):
    """Generate a website from prompt"""
    try:
        # Generate unique ID
        website_id = str(uuid.uuid4())
        
        # Generate content based on prompt
        content = generate_website_content(request.prompt, request.template)
        
        # Build website
        website = build_website(content, request.template)
        
        # Store project
        projects[website_id] = {
            "id": website_id,
            "prompt": request.prompt,
            "template": request.template,
            "style": request.style,
            "created_at": datetime.now().isoformat(),
            **website
        }
        
        return WebsiteResponse(
            id=website_id,
            html=website["html"],
            css=website["css"],
            js=website["js"],
            metadata={
                "prompt": request.prompt,
                "template": request.template,
                "style": request.style,
                "created_at": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/preview/{website_id}")
async def preview_website(website_id: str):
    """Get website for preview"""
    if website_id not in projects:
        raise HTTPException(status_code=404, detail="Website not found")
    
    return projects[website_id]

@app.get("/api/export/{website_id}")
async def export_website(website_id: str):
    """Export website as downloadable files"""
    if website_id not in projects:
        raise HTTPException(status_code=404, detail="Website not found")
    
    project = projects[website_id]
    
    return {
        "id": website_id,
        "files": {
            "index.html": project["html"],
            "style.css": project["css"],
            "script.js": project["js"]
        },
        "metadata": project.get("metadata", {})
    }

@app.get("/api/projects")
async def list_projects():
    """List all generated projects"""
    return {
        "projects": [
            {
                "id": project_id,
                "prompt": project["prompt"],
                "template": project.get("template"),
                "created_at": project["created_at"]
            }
            for project_id, project in projects.items()
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
