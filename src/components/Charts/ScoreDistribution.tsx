import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

interface ScoreDistributionProps {
  data: Array<{
    range: string;
    count: number;
  }>;
}

const COLORS = {
  'very_high': 'hsl(var(--destructive))',
  'high': 'hsl(var(--warning))',
  'medium': 'hsl(var(--chart-3))',
  'low': 'hsl(var(--success))',
};

const ScoreDistribution = ({ data }: ScoreDistributionProps) => {
  const getRiskTier = (range: string): string => {
    if (range.includes('750-850')) return 'low';
    if (range.includes('650-749')) return 'medium';
    if (range.includes('550-649')) return 'high';
    return 'very_high';
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Score Distribution</CardTitle>
        <CardDescription>Distribution of applicants across credit score ranges</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
            <XAxis 
              dataKey="range" 
              stroke="hsl(var(--muted-foreground))"
              fontSize={12}
            />
            <YAxis 
              stroke="hsl(var(--muted-foreground))"
              fontSize={12}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'hsl(var(--card))',
                border: '1px solid hsl(var(--border))',
                borderRadius: '8px',
              }}
            />
            <Bar dataKey="count" radius={[8, 8, 0, 0]}>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[getRiskTier(entry.range) as keyof typeof COLORS]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
};

export default ScoreDistribution;
