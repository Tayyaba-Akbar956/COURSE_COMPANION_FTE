# SPEC-T-003-content-storage-v1.0

## Status
- [x] Draft
- [ ] Pending Approval
- [ ] Approved
- [ ] In Progress
- [ ] Completed
- [ ] Deprecated

## Metadata
- **Created:** 2026-03-29
- **Author:** Qwen Code (AI Builder)
- **Approved By:** [Pending User Approval]
- **Version:** 1.0.0

## 1. Overview

This spec defines the content storage architecture for course materials including chapter content, images, diagrams, and media assets. We use a hybrid approach: chapter text in PostgreSQL (Supabase) and large assets (images, diagrams) in Cloudflare R2.

## 2. Storage Architecture

### 2.1 Hybrid Storage Model

| Content Type | Storage | Rationale |
|--------------|---------|-----------|
| Chapter text | PostgreSQL (Supabase) | Fast queries, transactional, versioned |
| Images/Diagrams | Cloudflare R2 | Cheap storage, CDN delivery, scalable |
| Code examples | PostgreSQL (Supabase) | Part of chapter content, searchable |
| Quiz questions | PostgreSQL (Supabase) | Relational data, needs joins |
| User progress | PostgreSQL (Supabase) | Relational, transactional |
| Videos (Phase 3) | Cloudflare Stream or Vimeo | Streaming optimized |

### 2.2 Why Cloudflare R2?

- **No egress fees** (unlike AWS S3)
- **S3-compatible API** (easy migration, familiar tools)
- **Built-in CDN** (fast global delivery)
- **Cheap storage** ($0.015/GB/month)
- **Free tier generous** (10GB storage, 10M reads/month)

## 3. Content Structure

### 3.1 Chapter Content Format

Chapters stored in PostgreSQL with this structure:

```json
{
  "id": 1,
  "chapter_number": 1,
  "module_id": 1,
  "title": "What is Generative AI?",
  "content": "# What is Generative AI?\n\nGenerative AI refers to...",
  "content_html": "<h1>What is Generative AI?</h1><p>Generative AI refers to...</p>",
  "is_free": true,
  "estimated_minutes": 15,
  "sections": [
    {
      "id": "section-1",
      "title": "Introduction",
      "content": "Generative AI refers to...",
      "order": 1
    },
    {
      "id": "section-2",
      "title": "Key Concepts",
      "content": "The main concepts are...",
      "order": 2
    }
  ],
  "images": [
    {
      "id": "img-1",
      "url": "https://r2.example.com/course/chapter-1/diagram-1.png",
      "alt": "Generative AI workflow diagram",
      "caption": "Figure 1.1: How generative AI works",
      "section_id": "section-1"
    }
  ],
  "code_examples": [
    {
      "id": "code-1",
      "language": "python",
      "code": "from transformers import pipeline\n\nclassifier = pipeline('sentiment-analysis')\nresult = classifier('I love AI!')\nprint(result)",
      "description": "Using Hugging Face transformers",
      "section_id": "section-2"
    }
  ]
}
```

### 3.2 R2 Bucket Structure

```
course-companion-fte/
├── generative-ai-fundamentals/
│   ├── chapter-1/
│   │   ├── diagram-1.png
│   │   ├── diagram-2.png
│   │   └── example-code-1.py
│   ├── chapter-2/
│   │   ├── architecture-diagram.png
│   │   └── comparison-chart.png
│   ├── chapter-3/
│   │   └── ...
│   └── ...
├── shared/
│   ├── logos/
│   │   ├── course-logo.png
│   │   └── panaversity-logo.png
│   ├── icons/
│   │   ├── achievement-badge.png
│   │   └── streak-flame.png
│   └── banners/
│       └── premium-upgrade-banner.png
└── user-generated/
    └── (Phase 3: user avatars, etc.)
```

## 4. Cloudflare R2 Setup

### 4.1 Bucket Creation

```bash
# Using Wrangler CLI
wrangler r2 bucket create course-companion-fte

# Output:
# ⛅ Creating bucket course-companion-fte with default storage class
# ✅ Created bucket course-companion-fte
```

### 4.2 Credentials

```bash
# Create R2 API token
wrangler r2 bucket info course-companion-fte

# Store in environment variables
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIs...
R2_ENDPOINT=https://xxx.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=xxx
R2_SECRET_ACCESS_KEY=xxx
R2_BUCKET_NAME=course-companion-fte
```

### 4.3 CORS Configuration

```json
{
  "CORSRules": [
    {
      "AllowedOrigins": [
        "https://your-app.vercel.app",
        "http://localhost:3000"
      ],
      "AllowedMethods": ["GET", "HEAD"],
      "AllowedHeaders": ["*"],
      "MaxAgeSeconds": 3600
    }
  ]
}
```

## 5. Backend Integration

### 5.1 R2 Client Setup

```python
import boto3
from botocore.config import Config
import os

def get_r2_client():
    """
    Create Cloudflare R2 client (S3-compatible)
    """
    return boto3.client(
        's3',
        endpoint_url=f"https://{os.getenv('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com",
        aws_access_key_id=os.getenv('R2_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('R2_SECRET_ACCESS_KEY'),
        config=Config(signature_version='s3v4'),
        region_name='auto'  # R2 is regionless
    )

r2_client = get_r2_client()
```

### 5.2 Upload Image to R2

```python
from fastapi import UploadFile, HTTPException
import uuid
from pathlib import Path

async def upload_chapter_image(
    file: UploadFile,
    chapter_id: int,
    user_id: str
) -> dict:
    """
    Upload image to R2 and return URL
    """
    # Validate file type
    allowed_types = ['image/png', 'image/jpeg', 'image/gif', 'image/svg+xml']
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Validate file size (max 5MB)
    file_size = 0
    content = await file.read()
    file_size = len(content)
    if file_size > 5 * 1024 * 1024:  # 5MB
        raise HTTPException(status_code=400, detail="File too large (max 5MB)")
    
    # Generate unique filename
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # R2 key path
    r2_key = f"generative-ai-fundamentals/chapter-{chapter_id}/{unique_filename}"
    
    try:
        # Upload to R2
        r2_client.put_object(
            Bucket=os.getenv('R2_BUCKET_NAME'),
            Key=r2_key,
            Body=content,
            ContentType=file.content_type,
            ACL='public-read'  # Make publicly accessible
        )
        
        # Construct CDN URL
        cdn_url = f"https://cdn.example.com/{r2_key}"
        
        return {
            "url": cdn_url,
            "r2_key": r2_key,
            "size": file_size,
            "content_type": file.content_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
```

### 5.3 Get Image from R2

```python
async def get_image_from_r2(r2_key: str) -> bytes:
    """
    Retrieve image from R2
    """
    try:
        response = r2_client.get_object(
            Bucket=os.getenv('R2_BUCKET_NAME'),
            Key=r2_key
        )
        return response['Body'].read()
    except Exception as e:
        raise HTTPException(status_code=404, detail="Image not found")
```

### 5.4 Delete Image from R2

```python
async def delete_image_from_r2(r2_key: str) -> bool:
    """
    Delete image from R2
    """
    try:
        r2_client.delete_object(
            Bucket=os.getenv('R2_BUCKET_NAME'),
            Key=r2_key
        )
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")
```

## 6. API Contract

### GET /api/v1/chapters/{chapter_id}

**Description:** Get chapter content (images referenced by URL)

**Request:**
```http
GET /api/v1/chapters/1
Authorization: Bearer {user_token}
```

**Response (200 OK):**
```json
{
  "chapter": {
    "id": 1,
    "title": "What is Generative AI?",
    "content": "# What is Generative AI?\n\n...",
    "images": [
      {
        "id": "img-1",
        "url": "https://cdn.example.com/generative-ai-fundamentals/chapter-1/abc-123.png",
        "alt": "Generative AI workflow diagram",
        "caption": "Figure 1.1: How generative AI works"
      }
    ],
    "code_examples": [
      {
        "language": "python",
        "code": "from transformers import pipeline...",
        "description": "Using Hugging Face transformers"
      }
    ]
  }
}
```

### POST /api/v1/chapters/{chapter_id}/images

**Description:** Upload image for a chapter

**Request:**
```http
POST /api/v1/chapters/1/images
Authorization: Bearer {user_token}
Content-Type: multipart/form-data

file: [image file]
alt: "Generative AI workflow diagram"
caption: "Figure 1.1: How generative AI works"
```

**Response (201 Created):**
```json
{
  "success": true,
  "image": {
    "id": "img-1",
    "url": "https://cdn.example.com/generative-ai-fundamentals/chapter-1/abc-123.png",
    "alt": "Generative AI workflow diagram",
    "caption": "Figure 1.1: How generative AI works",
    "size": 245678,
    "content_type": "image/png",
    "uploaded_at": "2026-03-29T12:00:00Z"
  }
}
```

### DELETE /api/v1/chapters/{chapter_id}/images/{image_id}

**Description:** Delete image from chapter

**Request:**
```http
DELETE /api/v1/chapters/1/images/img-1
Authorization: Bearer {user_token}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Image deleted successfully"
}
```

### GET /api/v1/images/{image_id}

**Description:** Get image metadata

**Request:**
```http
GET /api/v1/images/img-1
Authorization: Bearer {user_token}
```

**Response (200 OK):**
```json
{
  "image": {
    "id": "img-1",
    "url": "https://cdn.example.com/...",
    "alt": "Generative AI workflow diagram",
    "caption": "Figure 1.1: How generative AI works",
    "chapter_id": 1,
    "section_id": "section-1",
    "size": 245678,
    "content_type": "image/png",
    "uploaded_at": "2026-03-29T12:00:00Z",
    "uploaded_by": "user-uuid"
  }
}
```

## 7. Content Delivery Network (CDN)

### 7.1 Cloudflare CDN Setup

```
R2 Bucket → Cloudflare CDN → Edge Locations → Users
```

**Benefits:**
- Images served from edge (faster load times)
- Automatic image optimization
- Caching at edge (reduced R2 reads)
- DDoS protection

### 7.2 Custom Domain Configuration

```bash
# In Cloudflare Dashboard
# 1. Go to R2 → Buckets → course-companion-fte
# 2. Click "Custom Domains"
# 3. Add domain: cdn.example.com
# 4. Verify DNS records
```

### 7.3 Cache Headers

```python
# Set cache headers for images
cache_headers = {
    "Cache-Control": "public, max-age=31536000, immutable",  # 1 year
    "CDN-Cache-Control": "public, max-age=31536000",
}

r2_client.put_object(
    Bucket=os.getenv('R2_BUCKET_NAME'),
    Key=r2_key,
    Body=content,
    ContentType='image/png',
    Metadata=cache_headers
)
```

## 8. Image Optimization

### 8.1 Automatic Optimization

Use Cloudflare Images for on-the-fly optimization:

```python
# Original image in R2
# https://cdn.example.com/chapter-1/diagram-1.png

# Optimized variants (automatic)
# https://cdn.example.com/cdn-cgi/image/width=800/chapter-1/diagram-1.png
# https://cdn.example.com/cdn-cgi/image/width=400/chapter-1/diagram-1.png
# https://cdn.example.com/cdn-cgi/image/format=webp/chapter-1/diagram-1.png
```

### 8.2 Responsive Images

```html
<!-- Frontend usage -->
<img
  src="https://cdn.example.com/chapter-1/diagram-1.png"
  srcset="
    https://cdn.example.com/cdn-cgi/image/width=400/chapter-1/diagram-1.png 400w,
    https://cdn.example.com/cdn-cgi/image/width=800/chapter-1/diagram-1.png 800w,
    https://cdn.example.com/cdn-cgi/image/width=1200/chapter-1/diagram-1.png 1200w
  "
  sizes="(max-width: 600px) 400px, (max-width: 1000px) 800px, 1200px"
  alt="Generative AI workflow diagram"
/>
```

## 9. Cost Estimation

### 9.1 Storage Costs (Monthly)

| Item | Size | Quantity | Total |
|------|------|----------|-------|
| Chapter text (DB) | 50KB | 24 chapters | 1.2 MB |
| Images per chapter | 500KB | 5 images × 24 chapters | 60 MB |
| Shared assets | 100KB | 20 assets | 2 MB |
| **Total Storage** | | | **~63 MB** |

**Cost:** 63 MB × $0.015/GB = **$0.001/month** (essentially free)

### 9.2 Bandwidth Costs

| Operation | Monthly | Cost |
|-----------|---------|------|
| R2 Reads | 1M reads | Free (included) |
| CDN Requests | 100K requests | Free |
| Egress | Unlimited | **$0 (no egress fees!)** |

**Total Monthly Cost: ~$0.001** (well within free tier)

## 10. Backup Strategy

### 10.1 Database Backups

- Supabase automatic backups (daily)
- Point-in-time recovery (7 days)
- Export to SQL dump weekly

### 10.2 R2 Backups

```python
# Backup R2 bucket to another bucket (optional)
async def backup_r2_bucket():
    """
    Copy all objects to backup bucket
    """
    source_bucket = os.getenv('R2_BUCKET_NAME')
    backup_bucket = os.getenv('R2_BACKUP_BUCKET_NAME')
    
    # List all objects
    objects = r2_client.list_objects_v2(Bucket=source_bucket)
    
    for obj in objects['Contents']:
        # Copy to backup bucket
        r2_client.copy_object(
            CopySource={'Bucket': source_bucket, 'Key': obj['Key']},
            Bucket=backup_bucket,
            Key=obj['Key']
        )
```

### 10.3 Content Export

```python
async def export_all_content() -> dict:
    """
    Export all course content as JSON
    """
    chapters = await get_all_chapters()
    
    export_data = {
        "exported_at": datetime.now().isoformat(),
        "version": "1.0",
        "chapters": chapters
    }
    
    # Save to R2 backup
    r2_client.put_object(
        Bucket=os.getenv('R2_BACKUP_BUCKET_NAME'),
        Key=f"exports/course-export-{datetime.now().strftime('%Y%m%d')}.json",
        Body=json.dumps(export_data, indent=2)
    )
    
    return export_data
```

## 11. Security Considerations

### 11.1 Access Control

- R2 bucket private by default
- Public read only for specific prefixes (chapter images)
- User uploads restricted to specific folders
- Signed URLs for private content (Phase 3)

### 11.2 Content Validation

```python
async def validate_image_upload(file: UploadFile) -> bool:
    """
    Validate image before upload
    """
    # Check file type
    allowed_types = ['image/png', 'image/jpeg', 'image/gif', 'image/svg+xml']
    if file.content_type not in allowed_types:
        return False
    
    # Check file size
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:  # 5MB
        return False
    
    # Check for malicious content (basic)
    if b'<script>' in content.lower():
        return False
    
    return True
```

### 11.3 Rate Limiting

```python
@app.post("/api/v1/chapters/{chapter_id}/images")
@limiter.limit("10/hour")  # Prevent upload spam
async def upload_image(request: Request, chapter_id: int, file: UploadFile):
    # Upload logic
```

## 12. Testing Requirements

### Test Scenarios

```python
def test_content_storage_upload_image():
    """Should upload image to R2 successfully"""
    # Arrange: Valid image file
    # Act: POST /api/v1/chapters/1/images
    # Assert: 201 Created, URL returned, image accessible

def test_content_storage_invalid_file_type():
    """Should reject invalid file types"""
    # Arrange: PDF file (not image)
    # Act: POST /api/v1/chapters/1/images
    # Assert: 400 Bad Request, error message

def test_content_storage_file_too_large():
    """Should reject files over 5MB"""
    # Arrange: 6MB image file
    # Act: POST /api/v1/chapters/1/images
    # Assert: 400 Bad Request, size error

def test_content_storage_delete_image():
    """Should delete image from R2"""
    # Arrange: Existing image in R2
    # Act: DELETE /api/v1/chapters/1/images/img-1
    # Assert: 200 OK, image no longer accessible

def test_content_storage_cdn_delivery():
    """Should serve images via CDN"""
    # Arrange: Image uploaded to R2
    # Act: GET image URL
    # Assert: Image served from cdn.example.com, correct cache headers

def test_content_storage_chapter_content():
    """Should store and retrieve chapter content from database"""
    # Arrange: Chapter content in database
    # Act: GET /api/v1/chapters/1
    # Assert: Content returned with images, code examples
```

## 13. Open Questions

1. **Video Storage:** Should we use Cloudflare Stream or Vimeo for video content (Phase 3)?
2. **User Avatars:** Should user avatars be stored in R2 or use Gravatar?
3. **Content Versioning:** Should we version chapter content (v1, v2, etc.)?
4. **Image Compression:** Should we compress images before upload or rely on CDN?
5. **Backup Frequency:** How often to backup R2 bucket (daily, weekly, on-change)?

## 14. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-03-29 | Initial draft | Qwen Code |

---

## 📋 APPROVAL REQUEST

**What:** Content Storage Spec (SPEC-T-003-content-storage-v1.0)  
**Why:** Defines how course content and media assets are stored and delivered  
**Files Affected:** 
- `docs/specs/technical/SPEC-T-003-content-storage-v1.0.md`

**Key Decisions:**
- Hybrid storage: PostgreSQL (text) + Cloudflare R2 (images)
- R2 for no egress fees and built-in CDN
- S3-compatible API (boto3 library)
- Custom CDN domain (cdn.example.com)
- Automatic image optimization via Cloudflare
- 5MB max file size for uploads
- 1-year cache headers for images
- Cost: ~$0.001/month (essentially free)

**Do you approve this spec?** (Yes/No/Modify)

---

**Progress Update:**
- ✅ Phase 1 Feature Specs: 6/6 Complete
- ✅ Technical Specs: 3/3 Complete (ALL DONE!)
- ⏳ API Specs: 0/5 Remaining

**Next:** Create API Specs (SPEC-A-001 through SPEC-A-005)
