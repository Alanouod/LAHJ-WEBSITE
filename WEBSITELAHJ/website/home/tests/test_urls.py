
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from home.views import home, resource, inspiration, findPro, signup, user_login, joinAsPro, services, reso1, refe, tips, privacy_policy, terms_of_use, logout_view, professional_profile, homeowner_profile, cost, classic, edit_profile, edit_photo, save_photo_changes, edit_professional_profile, edit_professional_photo, Scandinavian, projects, add_project, project_details, save_to_wishlist, submit_rating
from home.views import *

class TestUrls(SimpleTestCase):
    def test_home_url_resolvesd(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, home)

    def test_resource_url_resolves(self):
        url = reverse('resource')
        self.assertEqual(resolve(url).func, resource)

    def test_inspiration_url_resolves(self):
        url = reverse('inspiration')
        self.assertEqual(resolve(url).func, inspiration)

    def test_findPro_url_resolves(self):
        url = reverse('findPro')
        self.assertEqual(resolve(url).func, findPro)

    def test_signup_url_resolves(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func, signup)

    def test_user_login_url_resolves(self):
        url = reverse('user_login')
        self.assertEqual(resolve(url).func, user_login)

    def test_joinAsPro_url_resolves(self):
        url = reverse('joinAsPro')
        self.assertEqual(resolve(url).func, joinAsPro)
    
    def test_reso1_url_resolves(self):
        url = reverse('reso1')
        self.assertEqual(resolve(url).func, reso1)
    
    def test_refe_url_resolves(self):
        url = reverse('refe')
        self.assertEqual(resolve(url).func, refe)
    
    def test_tips_url_resolves(self):
        url = reverse('tips')
        self.assertEqual(resolve(url).func, tips)
    
    def test_privacy_policy_url_resolves(self):
        url = reverse('privacy_policy')
        self.assertEqual(resolve(url).func, privacy_policy)
    
    def test_terms_of_use_url_resolves(self):
        url = reverse('terms_of_use')
        self.assertEqual(resolve(url).func, terms_of_use)
    
    def test_logout_view_url_resolves(self):
        url = reverse('logout_view')
        self.assertEqual(resolve(url).func, logout_view)
    
    def test_homeowner_profile_url_resolves(self):
        url = reverse('homeowner_profile')
        self.assertEqual(resolve(url).func, homeowner_profile)
    
    def test_professional_profile_url_resolves(self):
        url = reverse('professional_profile')
        self.assertEqual(resolve(url).func, professional_profile)
    def test_professional_profile_url_resolves(self):
        professional_id = 1
        url = reverse('professional_profile', kwargs={'professional_id': professional_id})
        self.assertEqual(resolve(url).func, professional_profile)
  
    def test_projects_url_resolves(self):
        url = reverse('projects')
        self.assertEqual(resolve(url).func, projects)
    
    def test_cost_url_resolves(self):
        url = reverse('cost')
        self.assertEqual(resolve(url).func, cost)
    
    def test_classic_url_resolves(self):
        url = reverse('classic')
        self.assertEqual(resolve(url).func, classic)
    
    def test_edit_profile_url_resolves(self):
        url = reverse('edit_profile')
        self.assertEqual(resolve(url).func, edit_profile)
    
    def test_edit_photo_url_resolves(self):
        url = reverse('edit_photo')
        self.assertEqual(resolve(url).func, edit_photo)
    
    def test_edit_professional_profile_url_resolves(self):
        url = reverse('edit_professional_profile')
        self.assertEqual(resolve(url).func, edit_professional_profile)
    
    def test_edit_professional_photo_url_resolves(self):
        url = reverse('edit_professional_photo')
        self.assertEqual(resolve(url).func, edit_professional_photo)
    
    def test_Scandinavian_url_resolves(self):
        url = reverse('Scandinavian')
        self.assertEqual(resolve(url).func, Scandinavian)
    
    def test_add_project_url_resolves(self):
        url = reverse('add_project')
        self.assertEqual(resolve(url).func, add_project)
    
    def test_wishlist_photos_url_resolves(self):
        url = reverse('wishlist_photos')
        self.assertEqual(resolve(url).func, wishlist_photos)
    
    def test_submit_rating_url_resolves(self):
        url = reverse('submit_rating')
        self.assertEqual(resolve(url).func, submit_rating)
   



