# Portfolio Rebuild Prompt - Usage Guide

## Overview
This JSON prompt (`portfolio_rebuild_prompt.json`) contains a complete specification for rebuilding the SkyPardaz portfolio website from scratch. It includes all technical details, structure, features, and implementation requirements.

## How to Use This Prompt

### Option 1: Direct AI Prompt
Copy the entire JSON content and provide it to an AI with this instruction:

```
I need you to build a Django portfolio website from scratch based on this complete specification. 
Please read the entire JSON file carefully and implement all features exactly as specified.

[Paste the entire JSON content here]
```

### Option 2: Step-by-Step Implementation
The JSON is structured to allow step-by-step implementation:

1. **Project Setup**: Follow `technology_stack` and `project_structure`
2. **Django Configuration**: Use `django_settings` section
3. **Database Models**: Implement all models from `database_models`
4. **Admin Interface**: Configure using `admin_configuration`
5. **URLs and Views**: Implement from `url_patterns` and `views`
6. **Templates**: Build from `templates` specification
7. **Frontend**: Implement `frontend_features`, `css_styling`, and `javascript_functionality`
8. **Translation**: Set up using `translation_setup`
9. **Testing**: Follow `testing_checklist`

## Key Sections

### 1. Technology Stack
- Backend: Django 4.2.11+, Python 3.12, SQLite3
- Frontend: Three.js, GSAP, modern CSS
- Dependencies: Listed in requirements format

### 2. Database Models
- Complete field specifications
- Translation requirements
- Validation rules
- Image optimization details

### 3. Frontend Features
- Three.js starfield animation
- GSAP scroll animations
- Dark mode support
- RTL/Persian support
- Lazy loading
- Responsive design

### 4. Implementation Details
- Exact file paths
- Code structure
- Configuration values
- Performance optimizations

## Important Notes

1. **Modeltranslation Order**: Must be before django.contrib.admin in INSTALLED_APPS
2. **Translation Registration**: Import portfolio.translation in forms.py
3. **Image Optimization**: Automatic on PortfolioItem.save()
4. **RTL Support**: Separate CSS file (styles-fa.css) for Persian
5. **Mobile Performance**: Reduced Three.js particles on mobile

## Validation

The JSON has been validated and is ready to use. It contains:
- ✅ Complete model specifications
- ✅ All field types and constraints
- ✅ Admin configuration details
- ✅ URL patterns and views
- ✅ Template structure
- ✅ Frontend feature specifications
- ✅ CSS and JavaScript requirements
- ✅ Translation setup
- ✅ Deployment requirements

## File Location

The prompt file is located at:
```
portfolio_rebuild_prompt.json
```

## Next Steps

1. Review the JSON file to understand the complete specification
2. Provide it to an AI assistant or development team
3. Follow the implementation step by step
4. Use the testing checklist to verify all features

---

**Note**: This prompt is designed to be comprehensive and precise. It should enable an AI or developer to rebuild the entire website with all features, styling, and functionality intact.

