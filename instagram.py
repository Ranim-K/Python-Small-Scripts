import instaloader
import os
from pathlib import Path

def download_instagram_profile(profile_name, download_path="instagram_downloads"):
    """Download all posts, stories, and highlights from a public Instagram profile"""
    
    # Create the main download directory
    main_dir = Path(download_path) / profile_name
    main_dir.mkdir(parents=True, exist_ok=True)
    
    # Create subdirectories
    posts_dir = main_dir / "posts"
    stories_dir = main_dir / "stories"
    highlights_dir = main_dir / "highlights"
    
    for directory in [posts_dir, stories_dir, highlights_dir]:
        directory.mkdir(exist_ok=True)
    
    # Initialize instaloader
    L = instaloader.Instaloader(
        dirname_pattern=str(posts_dir),
        download_pictures=True,
        download_videos=True,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=True,
        compress_json=False,
        post_metadata_txt_pattern=""
    )
    
    try:
        # Get profile
        profile = instaloader.Profile.from_username(L.context, profile_name)
        print(f"Downloading content from: {profile.username}")
        print(f"Total posts: {profile.mediacount}")
        print(f"Total followers: {profile.followers}")
        
        # Download posts
        print("\nDownloading posts...")
        for post in profile.get_posts():
            L.download_post(post, target=profile.username)
        print("Posts download completed!")
        
        # Download stories
        print("\nDownloading stories...")
        L.dirname_pattern = str(stories_dir)
        for story in L.get_stories(userids=[profile.userid]):
            for item in story.get_items():
                L.download_storyitem(item, target=f"{profile.username}_stories")
        print("Stories download completed!")
        
        # Download highlights
        print("\nDownloading highlights...")
        L.dirname_pattern = str(highlights_dir)
        for highlight in L.get_highlights(user=profile):
            for item in highlight.get_items():
                L.download_storyitem(item, target=f"{profile.username}_highlights")
        print("Highlights download completed!")
        
        print(f"\n✅ All downloads completed successfully!")
        print(f"📁 Files saved in: {main_dir}")
        
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"❌ Profile '{profile_name}' does not exist.")
    except instaloader.exceptions.PrivateProfileNotFollowedException:
        print(f"❌ Profile '{profile_name}' is private. Login required.")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    # Get username from user
    username = input("Enter Instagram username: ").strip()
    
    if username:
        download_instagram_profile(username)
    else:
        print("Please enter a valid username.")