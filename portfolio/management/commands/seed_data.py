from django.core.management.base import BaseCommand
from portfolio.models import Hero, About, Service, PortfolioItem, ContactInfo


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))
        
        # Clear existing data (optional - comment out if you want to keep existing data)
        Hero.objects.all().delete()
        About.objects.all().delete()
        Service.objects.all().delete()
        PortfolioItem.objects.all().delete()
        # ContactInfo.objects.all().delete()  # Keep contact info
        
        # Create Hero
        hero, created = Hero.objects.get_or_create(
            id=1,
            defaults={
                'title_en': 'Welcome to SkyPardaz',
                'title_fa': 'به اسکای پرداز خوش آمدید',
                'subtitle_en': 'Creative Studio',
                'subtitle_fa': 'استودیوی خلاق',
                'description_en': 'We create amazing digital experiences that transform your ideas into reality. Our team of experts is dedicated to delivering innovative solutions that exceed expectations.',
                'description_fa': 'ما تجربیات دیجیتال شگفت‌انگیزی خلق می‌کنیم که ایده‌های شما را به واقعیت تبدیل می‌کند. تیم متخصص ما متعهد به ارائه راه‌حل‌های نوآورانه است که فراتر از انتظارات عمل می‌کند.',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created Hero'))
        else:
            self.stdout.write(self.style.WARNING('Hero already exists'))
        
        # Create About items
        about_data = [
            {
                'title_en': 'Who We Are',
                'title_fa': 'ما کیستیم',
                'content_en': 'SkyPardaz is a leading creative studio specializing in web development, design, and digital marketing. With years of experience, we help businesses establish a strong online presence.',
                'content_fa': 'اسکای پرداز یک استودیوی خلاق پیشرو است که در توسعه وب، طراحی و بازاریابی دیجیتال تخصص دارد. با سال‌ها تجربه، به کسب‌وکارها کمک می‌کنیم تا حضور قوی آنلاین داشته باشند.',
                'order': 1
            },
            {
                'title_en': 'Our Mission',
                'title_fa': 'ماموریت ما',
                'content_en': 'Our mission is to empower businesses through innovative digital solutions. We believe in creating meaningful connections between brands and their audiences.',
                'content_fa': 'ماموریت ما توانمندسازی کسب‌وکارها از طریق راه‌حل‌های دیجیتال نوآورانه است. ما به ایجاد ارتباطات معنادار بین برندها و مخاطبانشان اعتقاد داریم.',
                'order': 2
            },
            {
                'title_en': 'Why Choose Us',
                'title_fa': 'چرا ما را انتخاب کنید',
                'content_en': 'We combine creativity with technical expertise to deliver exceptional results. Our client-focused approach ensures that every project is tailored to meet your specific needs.',
                'content_fa': 'ما خلاقیت را با تخصص فنی ترکیب می‌کنیم تا نتایج استثنایی ارائه دهیم. رویکرد متمرکز بر مشتری ما اطمینان می‌دهد که هر پروژه متناسب با نیازهای خاص شما طراحی می‌شود.',
                'order': 3
            }
        ]
        
        for i, data in enumerate(about_data, 1):
            about, created = About.objects.get_or_create(
                id=i,
                defaults={
                    **data,
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created About item {i}'))
        
        # Create Services
        services_data = [
            {
                'title_en': 'Web Development',
                'title_fa': 'توسعه وب',
                'description_en': 'Custom web applications built with modern technologies. Responsive, fast, and scalable solutions for your business.',
                'description_fa': 'اپلیکیشن‌های وب سفارشی ساخته شده با تکنولوژی‌های مدرن. راه‌حل‌های واکنش‌گرا، سریع و مقیاس‌پذیر برای کسب‌وکار شما.',
                'icon_svg': '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>',
                'order': 1
            },
            {
                'title_en': 'UI/UX Design',
                'title_fa': 'طراحی رابط کاربری',
                'description_en': 'Beautiful and intuitive user interfaces that enhance user experience. We design with your users in mind.',
                'description_fa': 'رابط‌های کاربری زیبا و بصری که تجربه کاربری را بهبود می‌بخشند. ما با در نظر گیری کاربران شما طراحی می‌کنیم.',
                'icon_svg': '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><path d="M21 15l-5-5L5 21"></path></svg>',
                'order': 2
            },
            {
                'title_en': 'Digital Marketing',
                'title_fa': 'بازاریابی دیجیتال',
                'description_en': 'Strategic marketing campaigns that drive results. From SEO to social media, we help you reach your target audience.',
                'description_fa': 'کمپین‌های بازاریابی استراتژیک که نتایج را به ارمغان می‌آورند. از سئو تا شبکه‌های اجتماعی، ما به شما کمک می‌کنیم تا به مخاطبان هدف خود برسید.',
                'icon_svg': '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>',
                'order': 3
            },
            {
                'title_en': 'E-Commerce Solutions',
                'title_fa': 'راه‌حل‌های تجارت الکترونیک',
                'description_en': 'Complete e-commerce platforms that help you sell online. Secure payment processing and inventory management included.',
                'description_fa': 'پلتفرم‌های کامل تجارت الکترونیک که به شما کمک می‌کنند آنلاین بفروشید. پردازش امن پرداخت و مدیریت موجودی شامل می‌شود.',
                'icon_svg': '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>',
                'order': 4
            },
            {
                'title_en': 'Mobile Apps',
                'title_fa': 'اپلیکیشن موبایل',
                'description_en': 'Native and cross-platform mobile applications for iOS and Android. Reach your users wherever they are.',
                'description_fa': 'اپلیکیشن‌های موبایل بومی و چندپلتفرمی برای iOS و Android. به کاربران خود در هر کجا که هستند دسترسی پیدا کنید.',
                'icon_svg': '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"></rect><line x1="12" y1="18" x2="12.01" y2="18"></line></svg>',
                'order': 5
            },
            {
                'title_en': 'Brand Identity',
                'title_fa': 'هویت برند',
                'description_en': 'Complete brand identity packages including logo design, color schemes, and brand guidelines.',
                'description_fa': 'بسته‌های کامل هویت برند شامل طراحی لوگو، پالت رنگ و راهنمای برند.',
                'icon_svg': '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>',
                'order': 6
            }
        ]
        
        for i, data in enumerate(services_data, 1):
            service, created = Service.objects.get_or_create(
                id=i,
                defaults={
                    **data,
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created Service {i}'))
        
        # Create Portfolio Items
        portfolio_data = [
            {
                'title_en': 'E-Commerce Platform',
                'title_fa': 'پلتفرم تجارت الکترونیک',
                'description_en': 'A modern e-commerce platform with advanced features including shopping cart, payment gateway, and admin dashboard.',
                'description_fa': 'یک پلتفرم تجارت الکترونیک مدرن با ویژگی‌های پیشرفته شامل سبد خرید، درگاه پرداخت و داشبورد مدیریتی.',
                'portfolio_type': 'online',
                'url': 'https://example.com/ecommerce',
                'order': 1
            },
            {
                'title_en': 'Corporate Website',
                'title_fa': 'وب‌سایت شرکتی',
                'description_en': 'A professional corporate website with responsive design, showcasing company services and portfolio.',
                'description_fa': 'یک وب‌سایت شرکتی حرفه‌ای با طراحی واکنش‌گرا، نمایش خدمات و نمونه کارهای شرکت.',
                'portfolio_type': 'online',
                'url': 'https://example.com/corporate',
                'order': 2
            },
            {
                'title_en': 'Mobile App Design',
                'title_fa': 'طراحی اپلیکیشن موبایل',
                'description_en': 'UI/UX design for a fitness tracking mobile application with beautiful and intuitive interface.',
                'description_fa': 'طراحی رابط کاربری برای یک اپلیکیشن موبایل ردیابی تناسب اندام با رابط زیبا و بصری.',
                'portfolio_type': 'offline',
                'order': 3
            },
            {
                'title_en': 'Restaurant Website',
                'title_fa': 'وب‌سایت رستوران',
                'description_en': 'A beautiful restaurant website with online menu, reservation system, and gallery.',
                'description_fa': 'یک وب‌سایت زیبای رستوران با منوی آنلاین، سیستم رزرو و گالری.',
                'portfolio_type': 'online',
                'url': 'https://example.com/restaurant',
                'order': 4
            },
            {
                'title_en': 'Portfolio Website',
                'title_fa': 'وب‌سایت پورتفولیو',
                'description_en': 'A creative portfolio website for a photographer with stunning image galleries and smooth animations.',
                'description_fa': 'یک وب‌سایت پورتفولیو خلاق برای یک عکاس با گالری‌های تصویر خیره‌کننده و انیمیشن‌های نرم.',
                'portfolio_type': 'online',
                'url': 'https://example.com/portfolio',
                'order': 5
            },
            {
                'title_en': 'Dashboard Design',
                'title_fa': 'طراحی داشبورد',
                'description_en': 'A comprehensive admin dashboard with analytics, user management, and reporting features.',
                'description_fa': 'یک داشبورد مدیریتی جامع با تجزیه و تحلیل، مدیریت کاربران و ویژگی‌های گزارش‌دهی.',
                'portfolio_type': 'offline',
                'order': 6
            }
        ]
        
        for i, data in enumerate(portfolio_data, 1):
            portfolio, created = PortfolioItem.objects.get_or_create(
                id=i,
                defaults={
                    **data,
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created Portfolio Item {i}'))
        
        # Create Contact Info
        contact_info, created = ContactInfo.objects.get_or_create(
            id=1,
            defaults={
                'email': 'info@skypardaz.com',
                'phone': '+98 21 1234 5678',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created Contact Info'))
        else:
            self.stdout.write(self.style.WARNING('Contact Info already exists'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ All sample data created successfully!'))

