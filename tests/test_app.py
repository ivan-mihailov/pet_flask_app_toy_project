from app import Pet
import pytest


def test_new_pet():
    """
    Given a Pet model
    When a new pet is added
    Then check that the name and breed fields are defined correctly
    """
    pet = Pet('Jinx', 'Dog')
    assert pet.Name == 'Jinx'
    assert pet.Breed == 'Dog'
