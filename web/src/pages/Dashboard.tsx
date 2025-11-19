import React, { useEffect, useState } from 'react';
import { api } from '../lib/api';

const Dashboard = () => {
    const [stats, setStats] = useState({
        totalCrawls: 0,
        totalPages: 0,
        issuesFound: 0
    });

    useEffect(() => {
        api.getStats().then(setStats);
    }, []);

    return (
        <div className="space-y-6">
            <h1 className="text-3xl font-bold tracking-tight">Overview</h1>

            <div className="grid gap-4 md:grid-cols-3">
                <div className="p-6 rounded-xl border bg-card text-card-foreground shadow">
                    <div className="text-sm font-medium text-muted-foreground">Total Crawls</div>
                    <div className="text-2xl font-bold">{stats.totalCrawls}</div>
                </div>
                <div className="p-6 rounded-xl border bg-card text-card-foreground shadow">
                    <div className="text-sm font-medium text-muted-foreground">Pages Indexed</div>
                    <div className="text-2xl font-bold">{stats.totalPages}</div>
                </div>
                <div className="p-6 rounded-xl border bg-card text-card-foreground shadow">
                    <div className="text-sm font-medium text-muted-foreground">Issues Detected</div>
                    <div className="text-2xl font-bold">{stats.issuesFound}</div>
                </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
                <div className="col-span-4 p-6 rounded-xl border bg-card text-card-foreground shadow">
                    <h3 className="font-semibold leading-none tracking-tight mb-4">Recent Activity</h3>
                    <div className="space-y-4">
                        {/* Mock Activity List */}
                        <div className="flex items-center">
                            <div className="ml-4 space-y-1">
                                <p className="text-sm font-medium leading-none">Crawl finished: example.com</p>
                                <p className="text-sm text-muted-foreground">2 minutes ago</p>
                            </div>
                            <div className="ml-auto font-medium text-green-500">Completed</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
