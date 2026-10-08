# S&P 100 News
1. Get a free API key at https://finnhub.io
2. Create a GitHub repo, push these files.
3. Repo Settings > Secrets and variables > Actions: add secret FINNHUB_API_KEY.
4. Settings > Pages: deploy from the main branch (root).
5. Actions tab > "Update news" > Run workflow once. After that it refreshes every 30 minutes.
Test locally: FINNHUB_API_KEY=xxx python fetch_news.py && python -m http.server
