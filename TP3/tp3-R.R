muestra <- sample(seq(0, 1, by = 0.01), 100, replace = TRUE) # 100 numeros aleatorios

media <- mean(muestra) # Media

desvio_estandar <- sd(muestra) # Desvio estandar

varianza <- var(muestra) # Varianza

hist(muestra, breaks=10, col='lightblue', border='black', xlab='Valor', ylab='Frecuencia', main='Histograma de la muestra generada') # Histograma

abline(v=media, col='red', lwd=2) # Linea para mostrar la media
abline(v=c(media - desvio_estandar, media + desvio_estandar), col='blue', lwd=2, lty=2) # Linea de la desvio estandar

legend('topright', legend=c('Media', 'Desvio estandar'), col=c('red', 'blue'), lwd=2, lty=1:2) # Leyenda del grafico