# S3-compatible object storage

Uploaded files (user avatars, attachments, generated reports) usually live
in an S3-compatible bucket rather than the database, and get forgotten in a
backup drill that only thinks about the database. The same bucket API
(AWS S3, and compatible services) works across providers, so the same
commands apply wherever the project's storage lives.

## Finding the actual mechanism

A bucket is not automatically backed up just by existing. Look for one of:

- **Versioning** enabled on the bucket, which keeps prior versions of an
  object after it is overwritten or deleted, but does not protect against
  the whole bucket being removed.
- **Cross-region or cross-account replication**, which copies objects to a
  second bucket as they are written.
- **A scheduled sync job** copying the bucket's contents elsewhere.

If none of these are configured, the bucket has no backup regardless of
how reliable the storage provider's own durability claims are; note that
plainly rather than assuming durability equals recoverability.

## Restoring into a throwaway target

```bash
# List what is there, to know what the drill should restore
aws s3 ls s3://source-bucket/ --recursive --summarize --endpoint-url https://<endpoint>

# Sync into a separate, disposable bucket or local folder
aws s3 sync s3://source-bucket/ s3://throwaway-bucket/ --endpoint-url https://<endpoint>
```

`--endpoint-url` points the AWS CLI at a non-AWS S3-compatible provider;
omit it for AWS itself. `rclone sync` is an equally common alternative and
takes the same source and destination shape.

## What to check

Object count and total size compared with the source, and that a sample
of files (particularly ones referenced by a database row restored in the
same drill) open correctly rather than being zero-byte or truncated. A
sync that silently skipped files with unusual characters in their key is a
real, recurring failure mode worth checking for directly.
