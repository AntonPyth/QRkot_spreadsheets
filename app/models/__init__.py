from .charity_project import CharityProject
from .donation import Donation
from .user import User

CharityProject.investment_counterpart = Donation
Donation.investment_counterpart = CharityProject

__all__ = [
    'CharityProject',
    'Donation',
    'User',
]
