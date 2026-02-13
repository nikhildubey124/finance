"""
Cache Helpers - Cached Query Functions
======================================
This module provides cached versions of frequently accessed queries
to improve application performance.

Functions decorated with @cache.memoize will cache results for the
specified timeout period, reducing database load.
"""

from extensions import cache
from models import Category, User


@cache.memoize(timeout=600)  # Cache for 10 minutes
def get_all_categories():
    """
    Get all categories (system + user categories).
    Cached for 10 minutes to reduce database queries.
    """
    return Category.query.all()


@cache.memoize(timeout=600)
def get_categories_by_type(category_type):
    """
    Get categories filtered by type (CREDIT/DEBIT).
    Cached for 10 minutes.
    """
    return Category.query.filter_by(category_type=category_type).all()


@cache.memoize(timeout=600)
def get_user_categories(user_id):
    """
    Get all categories available to a specific user
    (system categories + user's custom categories).
    Cached for 10 minutes.
    """
    return Category.query.filter(
        (Category.user_id == None) | (Category.user_id == user_id)
    ).all()


@cache.memoize(timeout=600)
def get_user_categories_by_type(user_id, category_type):
    """
    Get user's available categories filtered by type.
    Cached for 10 minutes.
    """
    return Category.query.filter(
        ((Category.user_id == None) | (Category.user_id == user_id)),
        Category.category_type == category_type
    ).all()


def clear_category_cache():
    """
    Clear all category-related caches.
    Call this after creating, updating, or deleting categories.
    """
    cache.delete_memoized(get_all_categories)
    cache.delete_memoized(get_categories_by_type)
    cache.delete_memoized(get_user_categories)
    cache.delete_memoized(get_user_categories_by_type)


def invalidate_user_cache(user_id):
    """
    Invalidate cache for a specific user.
    Call this after user-specific data changes.
    """
    cache.delete_memoized(get_user_categories, user_id)
    # Note: For category type variations, you'd need to clear all types
    cache.delete_memoized(get_user_categories_by_type, user_id, 'CREDIT')
    cache.delete_memoized(get_user_categories_by_type, user_id, 'DEBIT')
