import { useNavigate } from 'react-router-dom'
import { Button, Card, CardBody } from "@heroui/react";
import { FileText, LogOut, BarChart3 } from "lucide-react";

const DashboardPage = () => {
  const navigate = useNavigate()

  const handleLogout = () => {
    navigate('/');
  };

  const handleDocuments = () => {
    navigate('/documents');
  };

  const handleStatistics = () => {
    navigate('/statistics');
  };

  return (
    <div style={styles.page}>
      {/* Header - как на StatisticsPage */}
      <div style={styles.header}>
        <div style={styles.spacer}></div>
        <h1 style={styles.title}>Админ-Панель</h1>
        <Button
          isIconOnly
          className="bg-transparent hover:bg-gray-200 rounded-full transition-colors"
          onClick={handleLogout}
        >
          <LogOut size={20} className="text-black" />
        </Button>
      </div>

      {/* Content Container */}
      <div style={styles.contentWrapper}>
        {/* Documents Card */}
        <Card className="border border-gray-200 shadow-md hover:shadow-lg transition-shadow" style={styles.card}>
          <CardBody className="gap-4 p-6" style={{display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center'}}>
            <FileText size={48} className="text-black" />
            <h2 style={styles.cardTitle}>Управление документами</h2>
            <p style={styles.cardDescription}>
              Нажмите кнопку ниже, чтобы перейти в раздел управления документами
            </p>
            <Button
              onClick={handleDocuments}
              className="bg-black text-white font-semibold uppercase rounded-lg px-6 py-2 w-full hover:bg-gray-900 transition-colors"
            >
              Перейти к документам
            </Button>
          </CardBody>
        </Card>

        {/* Statistics Card */}
        <Card className="border border-gray-200 shadow-md hover:shadow-lg transition-shadow" style={styles.card}>
          <CardBody className="gap-4 p-6" style={{display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center'}}>
            <BarChart3 size={48} className="text-black" />
            <h2 style={styles.cardTitle}>Статистика проекта</h2>
            <p style={styles.cardDescription}>
              Нажмите кнопку ниже, чтобы перейти в раздел статистики
            </p>
            <Button
              onClick={handleStatistics}
              className="bg-black text-white font-semibold uppercase rounded-lg px-6 py-2 w-full hover:bg-gray-900 transition-colors"
            >
              Перейти к статистике
            </Button>
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
  spacer: {
    width: "40px",
    height: "40px",
  },
  title: {
    fontSize: "28px",
    fontWeight: "700",
    color: "#000000",
    margin: 0,
    flex: 1,
    textAlign: "center",
  },
  contentWrapper: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    gap: "32px",
    flex: 1,
    maxWidth: "1200px",
    margin: "0 auto",
    width: "100%",
    flexWrap: "wrap",
  },
  card: {
    borderRadius: "12px",
    width: "350px",
    minHeight: "300px",
  },
  cardTitle: {
    fontSize: "20px",
    fontWeight: "700",
    color: "#000000",
    margin: 0,
  },
  cardDescription: {
    fontSize: "14px",
    color: "#666666",
    margin: 0,
    flex: 1,
  },
};

export default DashboardPage;
