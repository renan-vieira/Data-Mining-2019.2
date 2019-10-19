#===============================================
# PROJETO MINERACAO DE DADOS
# analise exploratoria e visualizacao de dados
#
# @claudioalvesmonteiro
#===============================================

# importar pacotes
library(ggplot2); library(dplyr)

# importar dados
data <- read.csv("data/preprocessed_data.csv")

# layout ggplot
tema_massa <- function (base_size = 12, base_family = "") {
  theme_minimal(base_size = base_size, base_family = base_family) %+replace% 
    theme(axis.text.x = element_text(colour="black", size=11,hjust=.5,vjust=.5,face="plain"),
          axis.text.y = element_text(colour="black", size=11,angle=0,hjust=1,vjust=0,face="plain"), 
          axis.title.x = element_text(colour="black",size=11,angle=0,hjust=.5,vjust=0,face="plain"),
          axis.title.y = element_text(colour="black",size=11,angle=90,hjust=0.5,vjust=0.6,face="plain"),
          title = element_text(colour="black",size=14,angle=0,hjust=.5,vjust=.5,face="plain"))
}


#============================
# Descritiva das numericas 
#============================

# Idade
ggplot(data=data, aes(data$Idade))+
  geom_histogram( fill = "#5c4963")+
  scale_x_continuous(breaks = pretty(data$Idade, n = 20)) +
  tema_massa()+
  labs(x='Idade', y='Frequência')+
  ggsave("plot_Idade.png", path = "data/tables/", width = 6, height = 4, units = "in")

# Peso
ggplot(data=data, aes(data$Peso))+
  geom_histogram( fill = "#5c4963")+
  scale_x_continuous(breaks = pretty(data$Peso, n = 20)) +
  tema_massa()+
  labs(x='Peso', y='Frequência')+
  ggsave("plot_Peso.png", path = "data/tables/", width = 6, height = 4, units = "in")

# Procedimento
ggplot(data=data, aes(data$numero_procedimentos))+
  geom_histogram( fill = "#5c4963")+
  scale_x_continuous(breaks = pretty(data$numero_procedimentos, n = 20)) +
  tema_massa()+
  labs(x='Procedimento', y='Frequência')+
  ggsave("plot_procedimentos.png", path = "data/tables/", width = 7, height = 4, units = "in")

#============================
# Descritiva das categoricas 
#============================

#--- sexo

sexo <- read.csv("data/tables/alvo_Sexo_TABLE.csv")

sexo = mutate(sexo, alvo2 = ifelse(Alvo == 1, 'Internado na UTI', 'Não Internado'))

ggplot(data=sexo, aes(x=alvo2, y=porcent, fill=sexo$Sexo))+
  geom_bar(stat="identity", position=position_dodge())+
  geom_text(aes(label = as.character(porcent)), vjust = -0.5,size = 3.5,
            position = position_dodge(width = 1))+
  scale_fill_manual("Sexo", values=c("#E69F00", "#5c4963"))+
  scale_y_continuous(limits = c(0, 80))+
  labs(x = "", y = paste("%"), title = "" )+
  tema_massa()

ggsave("plot_sexo_alvo.png", path = "data/tables", width = 6, height = 4, units = "in")

#---- CID

cid = read.csv("data/tables/CID_TABLE.csv")
cid = cid[cid$porcent >= 1,] 
cid$CID = factor(cid$CID, levels = cid$CID[order(cid$porcent)])

ggplot(data=cid, aes(x=cid$CID, y=cid$porcent))+
  geom_bar(stat="identity", fill='#5c4963')+
  geom_text(aes(label = as.character(round(porcent, 2))), hjust = -0.1,size = 3.5)+
  scale_y_continuous(limits = c(0, 30))+
  labs(x = "", y = paste("%"), title = "" )+
  coord_flip()+
  tema_massa()

ggsave("plot_CID.png", path = "data/tables", width = 4, height = 6, units = "in")

#---- Procedimentos

proc = read.csv("data/tables/PROCEDIMENTO_TABLE.csv")
proc = proc[proc$porcent >= 2,]

ggplot(data=proc, aes(x=proc$PROCEDIMENTO, y=proc$porcent))+
  geom_bar(stat="identity", fill='#5c4963')+
  geom_text(aes(label = as.character(round(porcent, 2))), hjust = -0.1,size = 3.5)+
  scale_y_continuous(limits = c(0, 10))+
  labs(x = "", y = paste("%"), title = "" )+
  coord_flip()+
  tema_massa()

ggsave("plot_Procedimento.png", path = "data/tables", width = 4, height = 6, units = "in")

