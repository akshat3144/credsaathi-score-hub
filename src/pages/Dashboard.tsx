import { useEffect, useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { useInsights } from "@/hooks/useInsights";
import { useNavigate } from "react-router-dom";
import Navbar from "@/components/Navbar";
import ApplicantCard from "@/components/ApplicantCard";
import ScoreDistribution from "@/components/Charts/ScoreDistribution";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Plus, Users, TrendingUp, AlertCircle } from "lucide-react";
import api from "@/services/api";
import { toast } from "sonner";

interface Applicant {
  id: string;
  name: string;
  email: string;
  phone?: string;
  credit_score?: number;
  risk_tier?: string;
  gig_data?: {
    platforms: string[];
    average_rating: number;
    total_gigs_completed: number;
  };
  financial_data?: any;
  social_data?: any;
}

const Dashboard = () => {
  const navigate = useNavigate();
  const [applicants, setApplicants] = useState<Applicant[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterTier, setFilterTier] = useState<string>("all");
  const [insightsOpen, setInsightsOpen] = useState(false);
  const [selectedApplicant, setSelectedApplicant] = useState<Applicant | null>(
    null
  );
  const {
    insights,
    loading: insightsLoading,
    error: insightsError,
    fetchInsights,
  } = useInsights();

  useEffect(() => {
    fetchApplicants();
  }, []);

  const fetchApplicants = async () => {
    try {
      const response = await api.get("/ingest/applicants");
      setApplicants(response.data);
    } catch (error: any) {
      console.error("Failed to fetch applicants:", error);
      toast.error("Failed to load applicants");
    } finally {
      setLoading(false);
    }
  };

  const handlePredict = async (applicantId: string) => {
    const toastId = toast.loading("Calculating credit score...");
    try {
      const response = await api.post("/predict/score", {
        applicant_id: applicantId,
      });
      toast.dismiss(toastId);
      toast.success(`Credit score calculated: ${response.data.score}`);

      // Refresh applicants to show updated score
      await fetchApplicants();

      // Navigate to result page
      navigate("/result", { state: { prediction: response.data } });
    } catch (error: any) {
      console.error("Prediction error:", error);
      toast.dismiss(toastId);
      toast.error(error.response?.data?.detail || "Failed to calculate score");
    }
  };

  const handleViewDetails = (applicantId: string) => {
    const applicant = applicants.find((a) => a.id === applicantId);
    if (applicant) {
      setSelectedApplicant(applicant);
      setInsightsOpen(true);
      fetchInsights(applicant);
    }
  };

  const filteredApplicants =
    filterTier === "all"
      ? applicants
      : applicants.filter((a) => a.risk_tier === filterTier);

  // Calculate statistics
  const totalApplicants = applicants.length;
  const scoredApplicants = applicants.filter((a) => a.credit_score).length;
  const avgScore =
    scoredApplicants > 0
      ? Math.round(
          applicants.reduce((sum, a) => sum + (a.credit_score || 0), 0) /
            scoredApplicants
        )
      : 0;

  // Score distribution data
  const scoreDistribution = [
    {
      range: "300-549",
      count: applicants.filter((a) => a.credit_score && a.credit_score < 550)
        .length,
    },
    {
      range: "550-649",
      count: applicants.filter(
        (a) => a.credit_score && a.credit_score >= 550 && a.credit_score < 650
      ).length,
    },
    {
      range: "650-749",
      count: applicants.filter(
        (a) => a.credit_score && a.credit_score >= 650 && a.credit_score < 750
      ).length,
    },
    {
      range: "750-850",
      count: applicants.filter((a) => a.credit_score && a.credit_score >= 750)
        .length,
    },
  ];

  // Render a section as a table
  function renderTable(obj: any): JSX.Element {
    if (!obj || typeof obj !== "object") return <span>{String(obj)}</span>;
    return (
      <table className="min-w-full border text-sm mb-2">
        <tbody>
          {Object.entries(obj).map(([k, v]) => (
            <tr key={k} className="border-b last:border-b-0">
              <td className="font-medium px-2 py-1 whitespace-nowrap align-top bg-muted/30">
                {k.replace(/_/g, " ")}
              </td>
              <td className="px-2 py-1 align-top">
                {Array.isArray(v)
                  ? v.map((item, idx) => (
                      <span key={idx} className="inline-block mr-1">
                        {typeof item === "object"
                          ? JSON.stringify(item)
                          : String(item)}
                        {idx < v.length - 1 ? ", " : ""}
                      </span>
                    ))
                  : typeof v === "object" && v !== null
                  ? renderTable(v)
                  : String(v)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      {/* Insights Dialog */}
      <Dialog open={insightsOpen} onOpenChange={setInsightsOpen}>
        <DialogContent className="max-w-6xl w-full overflow-y-auto max-h-[90vh]">
          <DialogHeader>
            <DialogTitle>Borrower Intelligence Report</DialogTitle>
            <DialogDescription>
              {selectedApplicant ? selectedApplicant.name : "Applicant"}
            </DialogDescription>
          </DialogHeader>
          {insightsLoading && <div>Loading insights...</div>}
          {insightsError && (
            <div className="text-destructive">{insightsError}</div>
          )}
          {insights && (
            <div className="space-y-4">
              {Object.entries(insights).map(([section, value]) => {
                // Render dashboard_output as a summary card, others as tables
                if (section === "dashboard_output") {
                  return (
                    <div
                      key={section}
                      className="border rounded p-3 bg-muted/10"
                    >
                      <div className="font-semibold mb-1 text-lg">
                        Decision & Summary
                      </div>
                      {renderTable(value)}
                    </div>
                  );
                }
                return (
                  <div key={section} className="border rounded p-3">
                    <div className="font-semibold mb-1 text-base">
                      {section.replace(/_/g, " ")}
                    </div>
                    {renderTable(value)}
                  </div>
                );
              })}
            </div>
          )}
        </DialogContent>
      </Dialog>

      <main className="container mx-auto px-4 py-8">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">Dashboard</h1>
            <p className="text-muted-foreground">
              Manage and score your applicants
            </p>
          </div>
          <Button onClick={() => navigate("/applicant-form")}>
            <Plus className="mr-2 h-4 w-4" />
            Add Applicant
          </Button>
        </div>

        {/* Statistics Cards */}
        <div className="mb-8 grid gap-4 md:grid-cols-3">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total Applicants
              </CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{totalApplicants}</div>
              <p className="text-xs text-muted-foreground">
                {scoredApplicants} scored
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Average Score
              </CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{avgScore}</div>
              <p className="text-xs text-muted-foreground">
                Across {scoredApplicants} applicants
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">High Risk</CardTitle>
              <AlertCircle className="h-4 w-4 text-destructive" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {
                  applicants.filter(
                    (a) => a.risk_tier === "high" || a.risk_tier === "very_high"
                  ).length
                }
              </div>
              <p className="text-xs text-muted-foreground">Require attention</p>
            </CardContent>
          </Card>
        </div>

        {/* Score Distribution Chart */}
        {scoredApplicants > 0 && (
          <div className="mb-8">
            <ScoreDistribution data={scoreDistribution} />
          </div>
        )}

        {/* Applicants List */}
        <Card>
          <CardHeader>
            <CardTitle>Applicants</CardTitle>
            <CardDescription>
              View and manage all applicant profiles
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs
              defaultValue="all"
              value={filterTier}
              onValueChange={setFilterTier}
            >
              <TabsList className="mb-4">
                <TabsTrigger value="all">All</TabsTrigger>
                <TabsTrigger value="low">Low Risk</TabsTrigger>
                <TabsTrigger value="medium">Medium Risk</TabsTrigger>
                <TabsTrigger value="high">High Risk</TabsTrigger>
              </TabsList>

              {loading ? (
                <div className="py-12 text-center text-muted-foreground">
                  Loading...
                </div>
              ) : filteredApplicants.length === 0 ? (
                <div className="py-12 text-center">
                  <p className="text-muted-foreground">No applicants found</p>
                  <Button
                    onClick={() => navigate("/applicant-form")}
                    className="mt-4"
                  >
                    <Plus className="mr-2 h-4 w-4" />
                    Add Your First Applicant
                  </Button>
                </div>
              ) : (
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                  {filteredApplicants.map((applicant) => (
                    <ApplicantCard
                      key={applicant.id}
                      applicant={applicant}
                      onPredict={handlePredict}
                      onViewDetails={handleViewDetails}
                    />
                  ))}
                </div>
              )}
            </Tabs>
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

export default Dashboard;
