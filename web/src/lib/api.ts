const API_URL = 'http://localhost:5000';

export const api = {
    async createProject(domain: string, userId: string) {
        const res = await fetch(`${API_URL}/projects`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ domain, user_id: userId }),
        });
        return res.json();
    },

    async startCrawl(projectId: string) {
        const res = await fetch(`${API_URL}/projects/${projectId}/crawl`, {
            method: 'POST',
        });
        return res.json();
    },

    async getPages(projectId: string) {
        const res = await fetch(`${API_URL}/projects/${projectId}/pages`);
        return res.json();
    },

    async getProjects() {
        const res = await fetch(`${API_URL}/projects`);
        return res.json();
    },

    async getIssues(projectId: string) {
        const res = await fetch(`${API_URL}/projects/${projectId}/issues`);
        return res.json();
    },

    async getStats() {
        // Mock stats for now, or implement endpoint
        return {
            totalCrawls: 0,
            totalPages: 0,
            issuesFound: 0
        }
    }
};
