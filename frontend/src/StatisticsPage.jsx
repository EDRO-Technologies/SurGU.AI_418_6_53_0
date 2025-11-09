import React from "react";
import { useNavigate } from 'react-router-dom'
import { Button, Card, CardBody } from "@heroui/react";
import { ArrowLeft, LogOut } from "lucide-react";

const StatisticsPage = () => {
  const navigate = useNavigate()

  const handleBack = () => {
    navigate('/dashboard');
  };

  const handleLogout = () => {
    navigate('/');
  };

  return (
    <div style={styles.page}>
      {/* Header */}
      <div style={styles.header}>
        <Button
          isIconOnly
          className="bg-transparent hover:bg-gray-100 rounded-lg transition-colors"
          onClick={handleBack}
        >
          <ArrowLeft size={20} className="text-black" />
        </Button>
        <h1 style={styles.title}>Статистика</h1>
        <Button
          isIconOnly
          className="bg-transparent hover:bg-gray-200 rounded-full transition-colors"
          onClick={handleLogout}
        >
          <LogOut size={20} className="text-black" />
        </Button>
      </div>

      {/* Content */}
      <div style={styles.container}>
        <Card className="border border-gray-200 shadow-sm" style={styles.card}>
          <CardBody className="gap-4 p-8" style={{textAlign: 'center'}}>
            <h2 style={styles.subtitle}>Здесь будет ваша статистика</h2>
            <p style={styles.description}>
              Эта страница готова для реализации различной статистики вашего проекта.
            </p>
          </CardBody>
        </Card>
      </div>
    </div>
  );
};

const styles = {
  page: {
    minHeight: "100vh",
    background: "#ffffff",
    padding: "20px",
    fontFamily: "'Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', sans-serif",
    display: "flex",
    flexDirection: "column",
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "40px",
    maxWidth: "1200px",
    margin: "0 auto 40px",
    width: "100%",
  },
  title: {
    fontSize: "28px",
    fontWeight: "700",
    color: "#000000",
    margin: 0,
  },
  container: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    maxWidth: "1200px",
    margin: "0 auto",
    width: "100%",
    flex: 1,
  },
  card: {
    borderRadius: "12px",
    maxWidth: "600px",
  },
  subtitle: {
    fontSize: "24px",
    fontWeight: "600",
    color: "#000000",
    margin: "0 0 16px 0",
  },
  description: {
    fontSize: "16px",
    color: "#666666",
    margin: 0,
  },
};

export default StatisticsPage;
