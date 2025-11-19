import React, { useState, useEffect } from 'react';
import { api } from '../lib/api';

interface Project {
    id: string;
    domain: string;
    created_at: string;
}

interface Issue {
    id: string;
    issue_type: string;
    severity: string;
    description: string;
    url: string;
    page_title: string;
}

export const Projects = () => {
    const [domain, setDomain] = useState('');
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');
    const [projects, setProjects] = useState<Project[]>([]);
    const [selectedProject, setSelectedProject] = useState<string | null>(null);
    const [issues, setIssues] = useState<Issue[]>([]);

    useEffect(() => {
        loadProjects();
    }, []);

    useEffect(() => {
        if (selectedProject) {
            loadIssues(selectedProject);
        }
    }, [selectedProject]);

    const loadProjects = async () => {
        try {
            const data = await api.getProjects();
            setProjects(data);
        } catch (err) {
            console.error("Failed to load projects", err);
        }
    };

    const loadIssues = async (projectId: string) => {
        try {
            const data = await api.getIssues(projectId);
            setIssues(data);
        } catch (err) {
            console.error("Failed to load issues", err);
        }
    };

    const handleCreate = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            const project = await api.createProject(domain, 'test-user-id');
            if (project.id) {
                setMessage(`Project created! ID: ${project.id}`);
                await api.startCrawl(project.id);
                setMessage(`Project created and crawl started! ID: ${project.id}`);
                loadProjects(); // Refresh list
            } else {
                setMessage('Error creating project');
            }
        } catch (err) {
            setMessage('Error creating project');
        }
        setLoading(false);
    };

    return (
        <div className="space-y-8">
            <h1 className="text-3xl font-bold tracking-tight">Projects</h1>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Create Project Form */}
                <div className="p-6 rounded-xl border bg-card text-card-foreground shadow">
                    <h3 className="font-semibold mb-4">Add New Project</h3>
                    <form onSubmit={handleCreate} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium mb-1">Domain</label>
                            <input
                                type="text"
                                value={domain}
                                onChange={(e) => setDomain(e.target.value)}
                                className="w-full p-2 rounded-md border bg-background"
                                placeholder="example.com"
                                required
                            />
                        </div>
                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full py-2 px-4 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 disabled:opacity-50"
                        >
                            {loading ? 'Creating...' : 'Start Crawl'}
                        </button>
                        {message && <p className="text-sm text-muted-foreground">{message}</p>}
                    </form>
                </div>

                {/* Project List */}
                <div className="p-6 rounded-xl border bg-card text-card-foreground shadow">
                    <h3 className="font-semibold mb-4">Your Projects</h3>
                    <div className="space-y-2">
                        {projects.map((p) => (
                            <div
                                key={p.id}
                                onClick={() => setSelectedProject(p.id)}
                                className={`p-3 rounded-md border cursor-pointer hover:bg-accent ${selectedProject === p.id ? 'bg-accent' : ''}`}
                            >
                                <div className="font-medium">{p.domain}</div>
                                <div className="text-xs text-muted-foreground">{new Date(p.created_at).toLocaleDateString()}</div>
                            </div>
                        ))}
                        {projects.length === 0 && <p className="text-sm text-muted-foreground">No projects yet.</p>}
                    </div>
                </div>
            </div>

            {/* Issues Report */}
            {selectedProject && (
                <div className="p-6 rounded-xl border bg-card text-card-foreground shadow">
                    <h3 className="font-semibold mb-4">SEO Issues Report</h3>
                    {issues.length === 0 ? (
                        <p className="text-muted-foreground">No issues found (or crawl pending).</p>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full text-sm text-left">
                                <thead className="text-xs text-muted-foreground uppercase bg-muted/50">
                                    <tr>
                                        <th className="px-4 py-3">Severity</th>
                                        <th className="px-4 py-3">Issue</th>
                                        <th className="px-4 py-3">Description</th>
                                        <th className="px-4 py-3">URL</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {issues.map((issue) => (
                                        <tr key={issue.id} className="border-b">
                                            <td className="px-4 py-3">
                                                <span className={`px-2 py-1 rounded-full text-xs font-medium ${issue.severity === 'critical' ? 'bg-red-100 text-red-800' :
                                                        issue.severity === 'high' ? 'bg-orange-100 text-orange-800' :
                                                            'bg-yellow-100 text-yellow-800'
                                                    }`}>
                                                    {issue.severity}
                                                </span>
                                            </td>
                                            <td className="px-4 py-3 font-medium">{issue.issue_type}</td>
                                            <td className="px-4 py-3">{issue.description}</td>
                                            <td className="px-4 py-3 text-muted-foreground truncate max-w-xs" title={issue.url}>{issue.url}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};
